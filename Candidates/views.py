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
        
    return render(request, 'candidates/profile.html', {'form': form})

@login_required
def interview_history(request):
    if request.user.role != 'CANDIDATE':
        return redirect('home')
        
    profile = request.user.candidate_profile
    past_interviews = profile.interviews.filter(status='COMPLETED').order_by('-scheduled_time')
    
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
        else:
            for error in list(form.errors.values()):
                messages.error(request, error[0])
    return redirect('candidate_profile')
