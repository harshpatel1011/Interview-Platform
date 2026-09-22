from django import forms
from Interviewers.models import Interview, InterviewerProfile

class AssignInterviewerForm(forms.ModelForm):
    scheduled_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500'})
    )
    interviewer = forms.ModelChoiceField(
        queryset=InterviewerProfile.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white'})
    )

    class Meta:
        model = Interview
        fields = ['interviewer', 'scheduled_time']
