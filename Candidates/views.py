from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CandidateRegistrationForm
from .models import CandidateProfile, AIPracticeSession

def register(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'CANDIDATE'
            user.save()
            
            # Create profile
            CandidateProfile.objects.create(user=user)
            
            login(request, user)
            return redirect('candidate_dashboard')
    else:
        form = CandidateRegistrationForm()
    
    return render(request, 'candidates/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.role != 'CANDIDATE':
        return redirect('home')
        
    profile = request.user.candidate_profile
    interviews = profile.interviews.all().order_by('-scheduled_time')[:2]
    
    # Fetch job offers from companies
    from Companies.models import UnlockTransaction
    offers = UnlockTransaction.objects.filter(candidate=profile, outcome__in=['OFFERED', 'HIRED', 'REJECTED']).order_by('-unlocked_at')
    
    return render(request, 'candidates/dashboard.html', {
        'profile': profile,
        'interviews': interviews,
        'offers': offers
    })

@login_required
def profile_view(request):
    if request.user.role != 'CANDIDATE':
        return redirect('home')
        
    profile = request.user.candidate_profile
    return render(request, 'candidates/profile.html', {'profile': profile})

@login_required
def profile_settings(request):
    if request.user.role != 'CANDIDATE':
        return redirect('home')
        
    profile = request.user.candidate_profile
    if request.method == 'POST':
        from .forms import CandidateProfileUpdateForm
        form = CandidateProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.name = form.cleaned_data['name']
            request.user.save()
            form.save()
            from django.contrib import messages
            messages.success(request, 'Profile updated successfully!')
            return redirect('candidate_profile')
    else:
        from .forms import CandidateProfileUpdateForm
        form = CandidateProfileUpdateForm(instance=profile, initial={'name': request.user.name})
        
    return render(request, 'candidates/settings.html', {'form': form})

@login_required
def interview_history(request):
    if request.user.role != 'CANDIDATE':
        return redirect('home')
        
    profile = request.user.candidate_profile
    past_interviews = profile.interviews.filter(status__in=['COMPLETED', 'CANCELLED']).order_by('-scheduled_time')
    
    return render(request, 'candidates/history.html', {'interviews': past_interviews})

@login_required
def delete_account(request):
    if request.method == 'POST' and request.user.role == 'CANDIDATE':
        user = request.user
        from django.contrib.auth import logout
        logout(request)
        user.delete()
        from django.contrib import messages
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    return redirect('candidate_profile')

@login_required
def change_password(request):
    if request.method == 'POST' and request.user.role == 'CANDIDATE':
        from django.contrib.auth.forms import PasswordChangeForm
        from django.contrib.auth import update_session_auth_hash
        from django.contrib import messages
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('candidate_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    return redirect('candidate_profile')

from Companies.models import JobPost, InterviewRequest

@login_required
def job_board(request):
    if request.user.role != 'CANDIDATE': return redirect('home')
    jobs = JobPost.objects.filter(is_active=True).order_by('-created_at')
    
    # Get jobs candidate already applied to
    applied_job_ids = InterviewRequest.objects.filter(
        candidate=request.user.candidate_profile, 
        requester='CANDIDATE'
    ).values_list('job_post_id', flat=True)
    
    return render(request, 'candidates/job_board.html', {
        'jobs': jobs,
        'applied_job_ids': applied_job_ids
    })

@login_required
def apply_job(request, job_id):
    if request.user.role != 'CANDIDATE': return redirect('home')
    
    if request.method == 'POST':
        profile = request.user.candidate_profile
        job = JobPost.objects.get(id=job_id)
        
        # Check if they need to pay
        if profile.interviews.count() > 0:
            request.session['pending_interview_action'] = {'type': 'job', 'job_id': job_id}
            return redirect('candidate_purchase_interview')
            
        InterviewRequest.objects.get_or_create(
            candidate=profile,
            company=job.company,
            job_post=job,
            requester='CANDIDATE',
            defaults={'status': 'PENDING'}
        )
        from django.contrib import messages
        messages.success(request, f"Successfully applied for {job.title} at {job.company.company_name}!")
        
    return redirect('candidate_job_board')

@login_required
def cancel_interview(request, interview_id):
    if request.user.role != 'CANDIDATE': return redirect('home')
    
    if request.method == 'POST':
        from django.shortcuts import get_object_or_404
        from Interviewers.models import Interview
        from django.contrib import messages
        
        interview = get_object_or_404(Interview, id=interview_id, candidate=request.user.candidate_profile)
        
        if interview.status == 'SCHEDULED':
            interview.status = 'CANCELLED'
            interview.save()
            
            # If this was their only active interview, set global status to PENDING
            profile = request.user.candidate_profile
            if not profile.interviews.filter(status='SCHEDULED').exists():
                profile.status = 'PENDING'
                profile.save()
                
            messages.success(request, f"Interview with {interview.interviewer.user.name} has been cancelled.")
        else:
            messages.warning(request, "You can only cancel scheduled interviews.")
            
    return redirect('candidate_dashboard')

@login_required
def cancel_request(request):
    if request.user.role != 'CANDIDATE': return redirect('home')
    
    if request.method == 'POST':
        profile = request.user.candidate_profile
        if profile.status == 'PENDING':
            # Revert to INTERVIEWED if they had previous, else REJECTED
            if profile.interviews.filter(status='COMPLETED').exists():
                profile.status = 'INTERVIEWED'
                from django.contrib import messages
                messages.success(request, "Your re-evaluation request has been cancelled.")
            else:
                profile.status = 'REJECTED'
                from django.contrib import messages
                messages.success(request, "Your initial interview request has been withdrawn.")
            profile.save()
            
    return redirect('candidate_request_interview')

@login_required
def request_interview(request):
    if request.user.role != 'CANDIDATE': return redirect('home')
    
    profile = request.user.candidate_profile
    
    if request.method == 'POST':
        if profile.status in ['INTERVIEWED', 'REJECTED']:
            if profile.interviews.count() > 0:
                request.session['pending_interview_action'] = {'type': 'reevaluation'}
                return redirect('candidate_purchase_interview')
                
            profile.status = 'PENDING'
            profile.save()
            return redirect('candidate_dashboard')
            
    scheduled_interview = profile.interviews.filter(status='SCHEDULED').first()
            
    return render(request, 'candidates/request_interview.html', {
        'profile': profile,
        'scheduled_interview': scheduled_interview
    })

@login_required
def purchase_interview(request):
    if request.user.role != 'CANDIDATE': return redirect('home')
    if 'pending_interview_action' not in request.session:
        return redirect('candidate_dashboard')
        
    return render(request, 'candidates/purchase_interview.html')

@login_required
def purchase_interview_success(request):
    if request.user.role != 'CANDIDATE': return redirect('home')
    
    if request.method == 'POST':
        action = request.session.get('pending_interview_action')
        if not action:
            return redirect('candidate_dashboard')
            
        profile = request.user.candidate_profile
        from django.contrib import messages
        
        if action['type'] == 'job':
            job = JobPost.objects.get(id=action['job_id'])
            InterviewRequest.objects.get_or_create(
                candidate=profile,
                company=job.company,
                job_post=job,
                requester='CANDIDATE',
                defaults={'status': 'PENDING'}
            )
            messages.success(request, f"Payment successful! Successfully applied for {job.title}.")
            del request.session['pending_interview_action']
            return redirect('candidate_job_board')
            
        elif action['type'] == 'reevaluation':
            profile.status = 'PENDING'
            profile.save()
            messages.success(request, "Payment successful! Re-evaluation requested successfully. You are back in the pending queue.")
            del request.session['pending_interview_action']
            return redirect('candidate_dashboard')
            
    return redirect('candidate_dashboard')

@login_required
def ai_practice_list(request):
    if request.user.role != 'CANDIDATE': return redirect('home')
    
    profile = request.user.candidate_profile
    sessions = profile.ai_sessions.all().order_by('-created_at')
    
    if request.method == 'POST':
        # Create session unconditionally (totally free)
        session = AIPracticeSession.objects.create(
            candidate=profile,
            is_free=True,
            status='IN_PROGRESS'
        )
        return redirect('candidate_ai_room', session_id=session.id)
            
    return render(request, 'candidates/ai_practice.html', {
        'sessions': sessions
    })

@login_required
def ai_practice_room(request, session_id):
    if request.user.role != 'CANDIDATE': return redirect('home')
    
    from django.shortcuts import get_object_or_404
    session = get_object_or_404(AIPracticeSession, id=session_id, candidate=request.user.candidate_profile)
    
    if session.status == 'COMPLETED':
        return redirect('candidate_ai_practice')
        
    return render(request, 'candidates/ai_room.html', {
        'session': session
    })

@login_required
def ai_practice_api(request, session_id):
    if request.user.role != 'CANDIDATE':
        from django.http import JsonResponse
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    if request.method == 'POST':
        import json
        from django.http import JsonResponse
        from django.utils import timezone
        
        session = AIPracticeSession.objects.get(id=session_id)
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'message':
            # Mock AI response
            user_msg = data.get('message', '').lower()
            response_text = "That's an interesting point. Can you elaborate more on how you would handle potential edge cases?"
            
            if 'hello' in user_msg or 'hi' in user_msg:
                response_text = "Hello! I am your AI Interviewer. Let's start. Can you tell me about a challenging project you recently worked on?"
            elif len(user_msg) < 10:
                response_text = "Could you provide a bit more detail?"
                
            return JsonResponse({'response': response_text})
            
        elif action == 'complete':
            import random
            session.status = 'COMPLETED'
            session.score = random.randint(65, 95)
            session.feedback = "Good communication skills. Demonstrated solid understanding of core concepts. Could improve on providing more specific examples when discussing problem-solving."
            session.transcript = json.dumps(data.get('transcript', []))
            session.completed_at = timezone.now()
            session.save()
            
            return JsonResponse({'redirect_url': '/candidate/ai-practice/'})
            
    return JsonResponse({'error': 'Invalid request'}, status=400)
