from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='management_dashboard'),
    path('assign/<int:candidate_id>/', views.assign_interviewer, name='management_assign'),
    
    # Candidate CRUD
    path('candidates/', views.candidate_list, name='management_candidate_list'),
    path('candidates/add/', views.candidate_create, name='management_candidate_create'),
    path('candidates/<int:id>/', views.candidate_detail, name='management_candidate_detail'),
    path('candidates/<int:id>/edit/', views.candidate_edit, name='management_candidate_edit'),
    path('candidates/<int:id>/delete/', views.candidate_delete, name='management_candidate_delete'),
    
    # Interviewer CRUD
    path('interviewers/', views.interviewer_list, name='management_interviewer_list'),
    path('interviewers/add/', views.interviewer_create, name='management_interviewer_create'),
    path('interviewers/<int:id>/', views.interviewer_detail, name='management_interviewer_detail'),
    path('interviewers/<int:id>/edit/', views.interviewer_edit, name='management_interviewer_edit'),
    path('interviewers/<int:id>/delete/', views.interviewer_delete, name='management_interviewer_delete'),
    
    # Interview CRUD
    path('interviews/', views.interview_list, name='management_interview_list'),
    path('interviews/add/', views.interview_create, name='management_interview_create'),
    path('interviews/<int:id>/edit/', views.interview_edit, name='management_interview_edit'),
    path('interviews/<int:id>/delete/', views.interview_delete, name='management_interview_delete'),
]
