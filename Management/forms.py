from django import forms
from Interviewers.models import Interview, InterviewerProfile

class AssignInterviewerForm(forms.ModelForm):
    scheduled_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500'}
        )
    )
    interviewer = forms.ModelChoiceField(
        queryset=InterviewerProfile.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white'})
    )

    designation = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white'})
    )

    class Meta:
        model = Interview
        fields = ['designation', 'interviewer', 'scheduled_time']
        
    def __init__(self, *args, **kwargs):
        candidate = kwargs.pop('candidate', None)
        super().__init__(*args, **kwargs)
        if candidate:
            roles = [r.strip() for r in (candidate.designations or 'Unspecified').split(',') if r.strip()]
            self.fields['designation'].choices = [(r, r) for r in roles]

from django.contrib.auth import get_user_model
from Candidates.models import CandidateProfile

User = get_user_model()

class CandidateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white', 'placeholder': 'Leave blank to keep unchanged'}))
    
    resume = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'}))
    status = forms.ChoiceField(choices=CandidateProfile.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'}))
    designations = forms.CharField(required=False, help_text="Comma-separated roles (e.g. Frontend Developer, Designer)", widget=forms.TextInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white', 'placeholder': 'e.g. Frontend Developer, Backend Developer'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            if hasattr(self.instance, 'candidate_profile'):
                profile = self.instance.candidate_profile
                self.fields['status'].initial = profile.status
                self.fields['designations'].initial = profile.designations
        else:
            self.fields['password'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        
        user.role = 'CANDIDATE'
        
        if commit:
            user.save()
            profile, _ = CandidateProfile.objects.get_or_create(user=user)
            
            if self.cleaned_data.get('resume'):
                profile.resume = self.cleaned_data['resume']
            
            profile.status = self.cleaned_data['status']
            if self.cleaned_data.get('designations') is not None:
                profile.designations = self.cleaned_data['designations']
                
            profile.save()
            
        return user


class InterviewerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white', 'placeholder': 'Leave blank to keep unchanged'}))
    
    department = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            if hasattr(self.instance, 'interviewer_profile'):
                profile = self.instance.interviewer_profile
                self.fields['department'].initial = profile.department
        else:
            self.fields['password'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
            
        user.role = 'INTERVIEWER'
        
        if commit:
            user.save()
            profile, _ = InterviewerProfile.objects.get_or_create(user=user)
            profile.department = self.cleaned_data.get('department')
            profile.save()
            
        return user


class InterviewCRUDForm(forms.ModelForm):
    candidate = forms.ModelChoiceField(
        queryset=CandidateProfile.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'})
    )
    interviewer = forms.ModelChoiceField(
        queryset=InterviewerProfile.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'})
    )
    designation = forms.CharField(
        required=True,
        widget=forms.Select(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'})
    )
    scheduled_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white placeholder-gray-500'}
        )
    )
    status = forms.ChoiceField(
        choices=Interview.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'})
    )

    class Meta:
        model = Interview
        fields = ['candidate', 'designation', 'interviewer', 'scheduled_time', 'status']

from .models import Question

class QuestionForm(forms.ModelForm):
    designation = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white placeholder-gray-500', 'placeholder': 'e.g. Frontend Developer'})
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white placeholder-gray-500', 'rows': 3, 'placeholder': 'Write the question here...'})
    )
    expected_answer = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white placeholder-gray-500', 'rows': 3, 'placeholder': 'What should the interviewer look for?'})
    )

    class Meta:
        model = Question
        fields = ['designation', 'text', 'expected_answer']
