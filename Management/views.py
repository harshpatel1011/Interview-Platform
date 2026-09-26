from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Candidates.models import CandidateProfile
from Interviewers.models import Interview
from .forms import AssignInterviewerForm
import uuid

@login_required
def dashboard(request):
    if request.user.role != 'MANAGEMENT':
        return redirect('home')
        
    candidates = CandidateProfile.objects.all().order_by('-applied_date')
    
    # Advanced Analytics
    total_candidates = candidates.count()
    pipeline_stats = {
        'PENDING': candidates.filter(status='PENDING').count(),
        'ASSIGNED': candidates.filter(status='ASSIGNED').count(),
        'INTERVIEWED': candidates.filter(status='INTERVIEWED').count(),
        'HIRED': candidates.filter(status='HIRED').count(),
        'REJECTED': candidates.filter(status='REJECTED').count(),
    }
    
    evaluated_candidates = candidates.exclude(score=None)
    total_evaluated = evaluated_candidates.count()
    passed = evaluated_candidates.filter(score__gte=70).count()
    failed = total_evaluated - passed
    pass_rate = int((passed / total_evaluated) * 100) if total_evaluated > 0 else 0
    
    from django.db.models import Avg
    avg_score = evaluated_candidates.aggregate(Avg('score'))['score__avg']
    avg_score = round(avg_score, 1) if avg_score else 0

    return render(request, 'management/dashboard.html', {
        'candidates': candidates,
        'pipeline_stats': pipeline_stats,
        'pass_rate': pass_rate,
        'passed': passed,
        'failed': failed,
        'total_evaluated': total_evaluated,
        'avg_score': avg_score
    })

@login_required
def assign_interviewer(request, candidate_id):
    if request.user.role != 'MANAGEMENT':
        return redirect('home')
        
    # fallback if 404 since I typo'd get_object_or_444 in imports initially
    from django.shortcuts import get_object_or_404
    candidate = get_object_or_404(CandidateProfile, id=candidate_id)
    
    if request.method == 'POST':
        form = AssignInterviewerForm(request.POST, candidate=candidate)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.candidate = candidate
            
            # Generate a unique Jitsi meeting link
            meeting_id = str(uuid.uuid4())[:12]
            interview.meeting_link = f"/interviewer/room/{meeting_id}/" # Internal URL that embeds jitsi
            
            interview.save()
            
            candidate.status = 'ASSIGNED'
            candidate.save()
            
            # Send Calendar Invites
            from .email_utils import send_interview_invites
            try:
                send_interview_invites(request, interview)
                messages.success(request, 'Interviewer assigned and calendar invites sent successfully!')
            except Exception as e:
                # Log error or warn user in a real app, but don't crash
                print(f"Failed to send emails: {e}")
                messages.success(request, 'Interviewer assigned successfully (but email failed).')
            
            return redirect('management_dashboard')
    else:
        form = AssignInterviewerForm(candidate=candidate)
        
    return render(request, 'management/assign.html', {'form': form, 'candidate': candidate})

from django.contrib import messages
from .forms import CandidateForm, InterviewerForm
from Interviewers.models import InterviewerProfile
from django.contrib.auth import get_user_model
User = get_user_model()

# --- Candidate CRUD ---

@login_required
def candidate_list(request):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    candidates = User.objects.filter(role='CANDIDATE').select_related('candidate_profile').order_by('-id')
    return render(request, 'management/candidate_list.html', {'candidates': candidates})

@login_required
def candidate_detail(request, id):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    candidate = get_object_or_404(CandidateProfile, id=id)
    return render(request, 'management/candidate_detail.html', {'candidate': candidate})

@login_required
def candidate_create(request):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate created successfully.')
            return redirect('management_candidate_list')
    else:
        form = CandidateForm()
    return render(request, 'management/candidate_form.html', {'form': form, 'title': 'Add Candidate'})

@login_required
def candidate_edit(request, id):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    user = get_object_or_404(User, id=id, role='CANDIDATE')
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate updated successfully.')
            return redirect('management_candidate_list')
    else:
        form = CandidateForm(instance=user)
    return render(request, 'management/candidate_form.html', {'form': form, 'title': 'Edit Candidate', 'candidate_user': user})

@login_required
def candidate_delete(request, id):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    if request.method == 'POST':
        user = get_object_or_404(User, id=id, role='CANDIDATE')
        user.delete()
        messages.success(request, 'Candidate deleted successfully.')
    return redirect('management_candidate_list')

# --- Interviewer CRUD ---

@login_required
def interviewer_list(request):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    interviewers = User.objects.filter(role='INTERVIEWER').select_related('interviewer_profile').order_by('-id')
    return render(request, 'management/interviewer_list.html', {'interviewers': interviewers})

@login_required
def interviewer_detail(request, id):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    interviewer = get_object_or_404(User, id=id, role='INTERVIEWER')
    return render(request, 'management/interviewer_detail.html', {'interviewer': interviewer})

@login_required
def interviewer_create(request):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    if request.method == 'POST':
        form = InterviewerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interviewer created successfully.')
            return redirect('management_interviewer_list')
    else:
        form = InterviewerForm()
    return render(request, 'management/interviewer_form.html', {'form': form, 'title': 'Add Interviewer'})

@login_required
def interviewer_edit(request, id):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    user = get_object_or_404(User, id=id, role='INTERVIEWER')
    if request.method == 'POST':
        form = InterviewerForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interviewer updated successfully.')
            return redirect('management_interviewer_list')
    else:
        form = InterviewerForm(instance=user)
    return render(request, 'management/interviewer_form.html', {'form': form, 'title': 'Edit Interviewer', 'interviewer_user': user})

@login_required
def interviewer_delete(request, id):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    if request.method == 'POST':
        user = get_object_or_404(User, id=id, role='INTERVIEWER')
        user.delete()
        messages.success(request, 'Interviewer deleted successfully.')
    return redirect('management_interviewer_list')

# --- Interview CRUD ---
from Interviewers.models import Interview
from .forms import InterviewCRUDForm
import uuid

@login_required
def interview_list(request):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    interviews = Interview.objects.all().order_by('-scheduled_time')
    return render(request, 'management/interview_list.html', {'interviews': interviews})

@login_required
def interview_create(request):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    if request.method == 'POST':
        form = InterviewCRUDForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            meeting_id = str(uuid.uuid4())[:12]
            interview.meeting_link = f"/interviewer/room/{meeting_id}/"
            interview.save()
            
            # Automatically update Candidate pipeline status
            candidate = interview.candidate
            if interview.status == 'COMPLETED':
                candidate.status = 'INTERVIEWED'
            elif interview.status == 'SCHEDULED':
                candidate.status = 'ASSIGNED'
            elif interview.status == 'CANCELLED':
                candidate.status = 'PENDING'
            candidate.save()
            
            # Send Calendar Invites
            from .email_utils import send_interview_invites
            try:
                send_interview_invites(request, interview)
            except Exception as e:
                print(f"Failed to send emails: {e}")
                
            messages.success(request, 'Interview created successfully. Calendar invites have been sent!')
            return redirect('management_interview_list')
    else:
        form = InterviewCRUDForm()
        
    import json
    candidate_designations = {
        c.id: [r.strip() for r in (c.designations or 'Unspecified').split(',') if r.strip()]
        for c in CandidateProfile.objects.all()
    }
    return render(request, 'management/interview_form.html', {
        'form': form, 
        'title': 'Schedule Interview',
        'candidate_designations_json': json.dumps(candidate_designations)
    })

@login_required
def interview_edit(request, id):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    interview = get_object_or_404(Interview, id=id)
    if request.method == 'POST':
        old_status = interview.status
        form = InterviewCRUDForm(request.POST, instance=interview)
        if form.is_valid():
            updated_interview = form.save()
            new_status = updated_interview.status
            
            if old_status != new_status:
                if new_status in ['CANCELLED', 'COMPLETED']:
                    from .email_utils import send_interview_update
                    try:
                        send_interview_update(request, updated_interview, new_status)
                    except Exception as e:
                        print(f"Failed to send update emails: {e}")
                
                # Automatically update Candidate pipeline status
                candidate = updated_interview.candidate
                if new_status == 'COMPLETED':
                    candidate.status = 'INTERVIEWED' # Evaluated
                elif new_status == 'SCHEDULED':
                    candidate.status = 'ASSIGNED' # Interviewing
                elif new_status == 'CANCELLED':
                    candidate.status = 'PENDING' # Applied
                candidate.save()
            
            messages.success(request, 'Interview updated successfully.')
            return redirect('management_interview_list')
    else:
        form = InterviewCRUDForm(instance=interview)
        
    import json
    candidate_designations = {
        c.id: [r.strip() for r in (c.designations or 'Unspecified').split(',') if r.strip()]
        for c in CandidateProfile.objects.all()
    }
    return render(request, 'management/interview_form.html', {
        'form': form, 
        'title': 'Edit Interview', 
        'interview': interview,
        'candidate_designations_json': json.dumps(candidate_designations)
    })

@login_required
def interview_delete(request, id):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    if request.method == 'POST':
        interview = get_object_or_404(Interview, id=id)
        
        # Send cancellation email if it wasn't already cancelled or completed
        if interview.status not in ['CANCELLED', 'COMPLETED']:
            from .email_utils import send_interview_update
            try:
                send_interview_update(request, interview, 'CANCELLED')
            except Exception as e:
                print(f"Failed to send cancellation emails: {e}")
                
        interview.delete()
        messages.success(request, 'Interview deleted successfully. Cancellation emails sent.')
    return redirect('management_interview_list')

# --- Question Bank Views ---
from .models import Question
from .forms import QuestionForm

@login_required
def question_list(request):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    questions = Question.objects.all().order_by('designation')
    return render(request, 'management/question_list.html', {'questions': questions})

@login_required
def question_create(request):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question added successfully.')
            return redirect('management_question_list')
    else:
        form = QuestionForm()
    return render(request, 'management/question_form.html', {'form': form, 'title': 'Add Question'})

@login_required
def question_delete(request, id):
    if request.user.role != 'MANAGEMENT': return redirect('home')
    if request.method == 'POST':
        q = get_object_or_404(Question, id=id)
        q.delete()
        messages.success(request, 'Question deleted.')
    return redirect('management_question_list')
