from django import forms
from .models import Interview

class ScoreForm(forms.ModelForm):
    technical_score = forms.IntegerField(
        min_value=0, max_value=40,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 bg-[#111] border border-white/10 rounded-lg text-white placeholder-gray-500 text-sm', 'placeholder': '0-40'})
    )
    problem_solving_score = forms.IntegerField(
        min_value=0, max_value=25,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 bg-[#111] border border-white/10 rounded-lg text-white placeholder-gray-500 text-sm', 'placeholder': '0-25'})
    )
    communication_score = forms.IntegerField(
        min_value=0, max_value=15,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 bg-[#111] border border-white/10 rounded-lg text-white placeholder-gray-500 text-sm', 'placeholder': '0-15'})
    )
    culture_fit_score = forms.IntegerField(
        min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 bg-[#111] border border-white/10 rounded-lg text-white placeholder-gray-500 text-sm', 'placeholder': '0-10'})
    )
    confidence_score = forms.IntegerField(
        min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 bg-[#111] border border-white/10 rounded-lg text-white placeholder-gray-500 text-sm', 'placeholder': '0-10'})
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full p-3.5 bg-[#111] border border-white/10 rounded-xl text-white placeholder-gray-500', 'rows': 4, 'placeholder': 'Detailed feedback...'})
    )

    class Meta:
        model = Interview
        fields = ['technical_score', 'problem_solving_score', 'communication_score', 'culture_fit_score', 'confidence_score', 'feedback']

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
