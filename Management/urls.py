from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='management_dashboard'),
    path('assign/<int:candidate_id>/', views.assign_interviewer, name='management_assign'),
    
    # Candidate View & Delete
    path('candidates/', views.candidate_list, name='management_candidate_list'),
    path('candidates/<int:id>/', views.candidate_detail, name='management_candidate_detail'),
    path('candidates/<int:id>/delete/', views.candidate_delete, name='management_candidate_delete'),
    
    path('requests/', views.interview_requests, name='management_interview_requests'),
    
    path('revenue/', views.revenue_dashboard, name='management_revenue'),
    
    # Interviewer Approvals
    path('interviewers/', views.interviewer_list, name='management_interviewer_list'),
    path('interviewers/<int:id>/', views.interviewer_detail, name='management_interviewer_detail'),
    path('interviewers/<int:id>/verify/', views.interviewer_verify, name='management_interviewer_verify'),
    
    # Interview CRUD
    path('interviews/', views.interview_list, name='management_interview_list'),
    path('interviews/add/', views.interview_create, name='management_interview_create'),
    path('interviews/<int:id>/edit/', views.interview_edit, name='management_interview_edit'),
    path('interviews/<int:id>/delete/', views.interview_delete, name='management_interview_delete'),
    
    # Company Approvals
    path('companies/', views.company_list, name='management_company_list'),
    path('companies/<int:id>/', views.company_detail, name='management_company_detail'),
    path('companies/<int:id>/verify/', views.company_verify, name='management_company_verify'),
    
    # Question Bank
    path('questions/', views.question_list, name='management_question_list'),
    path('questions/add/', views.question_create, name='management_question_create'),
    path('questions/<int:id>/delete/', views.question_delete, name='management_question_delete'),
    
]
