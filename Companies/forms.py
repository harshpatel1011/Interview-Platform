from django import forms
from django.contrib.auth import get_user_model
from .models import CompanyProfile

User = get_user_model()

class CompanyRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full bg-[#111] border border-white/10 rounded-lg p-3 text-white placeholder-gray-500 focus:border-primary focus:ring-1 focus:ring-primary outline-none transition', 'placeholder': 'Create a password'}))
    company_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'w-full bg-[#111] border border-white/10 rounded-lg p-3 text-white placeholder-gray-500 focus:border-primary focus:ring-1 focus:ring-primary outline-none transition', 'placeholder': 'Company Name'}))
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-[#111] border border-white/10 rounded-lg p-3 text-white placeholder-gray-500 focus:border-primary focus:ring-1 focus:ring-primary outline-none transition', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-[#111] border border-white/10 rounded-lg p-3 text-white placeholder-gray-500 focus:border-primary focus:ring-1 focus:ring-primary outline-none transition', 'placeholder': 'Work Email'}),
        }
