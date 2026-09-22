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
    return render(request, 'interviewers/dashboard.html', {'interviews': interviews})

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
                candidate.status = 'INTERVIEWED'
                candidate.save()
                
                return redirect('interviewer_dashboard')
        else:
            form = ScoreForm(instance=interview)
            
    return render(request, 'interviewers/room.html', {
        'interview': interview,
        'meeting_id': meeting_id,
        'form': form
    })
