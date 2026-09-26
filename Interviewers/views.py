from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Interview
from .forms import ScoreForm

@login_required
def dashboard(request):
    if request.user.role != 'INTERVIEWER':
        return redirect('home')
        
    profile = request.user.interviewer_profile
    interviews = profile.assigned_interviews.all().order_by('scheduled_time')
    
    # Calculate stats
    total_interviews = interviews.count()
    completed_interviews = interviews.filter(status='COMPLETED').count()
    upcoming_interviews = interviews.filter(status='SCHEDULED').count()
    
    return render(request, 'interviewers/dashboard.html', {
        'interviews': interviews,
        'total_interviews': total_interviews,
        'completed_interviews': completed_interviews,
        'upcoming_interviews': upcoming_interviews,
    })

@login_required
def profile_view(request):
    if request.user.role != 'INTERVIEWER':
        return redirect('home')
    
    profile = request.user.interviewer_profile
    return render(request, 'interviewers/profile.html', {'profile': profile})

@login_required
def profile_settings(request):
    if request.user.role != 'INTERVIEWER':
        return redirect('home')
        
    profile = request.user.interviewer_profile
    if request.method == 'POST':
        from .forms import InterviewerProfileUpdateForm
        form = InterviewerProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.name = form.cleaned_data['name']
            request.user.save()
            form.save()
            from django.contrib import messages
            messages.success(request, 'Profile updated successfully!')
            return redirect('interviewer_profile')
    else:
        from .forms import InterviewerProfileUpdateForm
        form = InterviewerProfileUpdateForm(instance=profile, initial={'name': request.user.name})
        
    return render(request, 'interviewers/settings.html', {'form': form})

@login_required
def video_room(request, meeting_id):
    # This view is accessible by candidate and interviewer.
    # We find the interview by checking if meeting_link ends with meeting_id
    interview = None
    for inv in Interview.objects.all():
        if inv.meeting_link and meeting_id in inv.meeting_link:
            interview = inv
            break
            
    if not interview:
        return redirect('home')
        
    # Check permissions
    if request.user.role == 'CANDIDATE' and interview.candidate.user != request.user:
        return redirect('home')
    if request.user.role == 'INTERVIEWER' and interview.interviewer.user != request.user:
        return redirect('home')

    form = None
    if request.user.role == 'INTERVIEWER':
        if request.method == 'POST':
            form = ScoreForm(request.POST, instance=interview)
            if form.is_valid():
                form.save()
                interview.status = 'COMPLETED'
                interview.save()
                
                # Update candidate global score (if multiple interviews, this overwrites, for simplicity)
                candidate = interview.candidate
                candidate.score = interview.score
                candidate.feedback = interview.feedback
                candidate.status = 'INTERVIEWED'
                candidate.save()
                
                return redirect('interviewer_dashboard')
        else:
            form = ScoreForm(instance=interview)
            
    # Fetch questions for the interviewer
    questions = []
    if request.user.role == 'INTERVIEWER':
        from Management.models import Question
        questions = Question.objects.filter(designation__icontains=interview.designation)
            
    return render(request, 'interviewers/room.html', {
        'interview': interview,
        'meeting_id': meeting_id,
        'form': form,
        'questions': questions
    })
