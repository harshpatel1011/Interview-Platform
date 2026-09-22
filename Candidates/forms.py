from django import forms
from django.contrib.auth import get_user_model
from .models import CandidateProfile

User = get_user_model()

class CandidateRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'placeholder': '••••••••'}))
    resume = forms.FileField(widget=forms.FileInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white'}))

    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'placeholder': 'name@example.com'}),
        }
