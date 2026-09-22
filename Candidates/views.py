from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CandidateRegistrationForm
from .models import CandidateProfile

def register(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'CANDIDATE'
            user.save()
            
            # Create profile
            CandidateProfile.objects.create(
                user=user,
                resume=request.FILES['resume']
            )
            
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
    interviews = profile.interviews.all().order_by('scheduled_time')
    
    return render(request, 'candidates/dashboard.html', {
        'profile': profile,
        'interviews': interviews
    })
