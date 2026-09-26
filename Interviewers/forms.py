from django import forms
from .models import Interview

class ScoreForm(forms.ModelForm):
    technical_score = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white placeholder-gray-500', 'placeholder': '0-100'})
    )
    communication_score = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white placeholder-gray-500', 'placeholder': '0-100'})
    )
    problem_solving_score = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white placeholder-gray-500', 'placeholder': '0-100'})
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white placeholder-gray-500', 'rows': 4, 'placeholder': 'Detailed feedback...'})
    )

    class Meta:
        model = Interview
        fields = ['technical_score', 'communication_score', 'problem_solving_score', 'feedback']

from .models import InterviewerProfile

class InterviewerProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white'})
    )
    
    class Meta:
        model = InterviewerProfile
        fields = ['department']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white'}),
        }
