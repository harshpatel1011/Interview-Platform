from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='interviewer_dashboard'),
    path('room/<str:meeting_id>/', views.video_room, name='interviewer_room'),
]
