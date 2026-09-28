from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    return render(request, 'home.html')

from django.shortcuts import redirect

def dashboard_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.role == 'CANDIDATE':
        return redirect('candidate_dashboard')
    elif request.user.role == 'INTERVIEWER':
        return redirect('interviewer_dashboard')
    elif request.user.role == 'MANAGEMENT':
        return redirect('management_dashboard')
    elif request.user.role == 'COMPANY':
        return redirect('company_dashboard')
        
    return redirect('home')

from django.views.generic import TemplateView

from Core import auth_views

from Interviewers.views import interview_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/password_reset/', auth_views.password_reset_request, name='password_reset'),
    path('accounts/password_reset/verify/', auth_views.password_reset_verify, name='password_reset_verify'),
    path('accounts/password_reset/confirm/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('accounts/', include('django.contrib.auth.urls')), # login/logout
    path('dashboard-redirect/', dashboard_redirect, name='dashboard_redirect'),
    path('interview/<int:id>/', interview_detail, name='interview_detail'),

    path('candidate/', include('Candidates.urls')),
    path('management/', include('Management.urls')),
    path('interviewer/', include('Interviewers.urls')),
    path('company/', include('Companies.urls')),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy.html'), name='privacy_policy'),
    path('terms-of-service/', TemplateView.as_view(template_name='terms.html'), name='terms_of_service'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
