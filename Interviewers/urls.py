from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='interviewer_dashboard'),
    path('profile/', views.profile_view, name='interviewer_profile'),
    path('settings/', views.profile_settings, name='interviewer_settings'),
    path('room/<str:meeting_id>/', views.video_room, name='interviewer_room'),
    path('earnings/', views.earnings, name='interviewer_earnings'),
    path('history/', views.history, name='interviewer_history'),
    path('register/', views.register, name='interviewer_register'),
]
