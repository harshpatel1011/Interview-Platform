from django import forms
from django.contrib.auth import get_user_model
from .models import CandidateProfile

User = get_user_model()

class CandidateRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'placeholder': '••••••••'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'placeholder': '••••••••'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'placeholder': 'name@example.com'}),
        }

class CandidateProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500'}))
    
    class Meta:
        model = CandidateProfile
        fields = ['resume', 'designations']
        widgets = {
            'resume': forms.FileInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white'}),
            'designations': forms.TextInput(attrs={'class': 'w-full p-3.5 premium-input rounded-xl text-white placeholder-gray-500', 'placeholder': 'Frontend Developer, Backend Engineer'}),
        }
