from django import forms
from .models import Interview

class ScoreForm(forms.ModelForm):
    score = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'placeholder': 'Score (0-100)'})
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'rows': 4, 'placeholder': 'Detailed feedback...'})
    )

    class Meta:
        model = Interview
        fields = ['score', 'feedback']
