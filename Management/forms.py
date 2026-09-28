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
        queryset=InterviewerProfile.objects.filter(is_verified=True),
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




class InterviewCRUDForm(forms.ModelForm):
    candidate = forms.ModelChoiceField(
        queryset=CandidateProfile.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white'})
    )
    interviewer = forms.ModelChoiceField(
        queryset=InterviewerProfile.objects.filter(is_verified=True),
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
