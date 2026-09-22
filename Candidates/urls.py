from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='candidate_dashboard'),
    path('register/', views.register, name='candidate_register'),
]
