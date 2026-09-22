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
    return render(request, 'management/dashboard.html', {'candidates': candidates})

@login_required
def assign_interviewer(request, candidate_id):
    if request.user.role != 'MANAGEMENT':
        return redirect('home')
        
    # fallback if 404 since I typo'd get_object_or_444 in imports initially
    from django.shortcuts import get_object_or_404
    candidate = get_object_or_404(CandidateProfile, id=candidate_id)
    
    if request.method == 'POST':
        form = AssignInterviewerForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.candidate = candidate
            
            # Generate a unique Jitsi meeting link
            meeting_id = str(uuid.uuid4())[:12]
            interview.meeting_link = f"/interviewer/room/{meeting_id}/" # Internal URL that embeds jitsi
            
            interview.save()
            
            candidate.status = 'ASSIGNED'
            candidate.save()
            
            return redirect('management_dashboard')
    else:
        form = AssignInterviewerForm()
        
    return render(request, 'management/assign.html', {'form': form, 'candidate': candidate})
