from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='candidate_dashboard'),
    path('register/', views.register, name='candidate_register'),
    path('profile/', views.profile_view, name='candidate_profile'),
    path('settings/', views.profile_settings, name='candidate_settings'),
    path('history/', views.interview_history, name='candidate_history'),
    path('delete_account/', views.delete_account, name='candidate_delete_account'),
    path('change_password/', views.change_password, name='candidate_change_password'),
]
