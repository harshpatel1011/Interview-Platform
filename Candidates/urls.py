from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='candidate_dashboard'),
    path('register/', views.register, name='candidate_register'),
    path('profile/', views.profile_view, name='candidate_profile'),
    path('settings/', views.profile_settings, name='candidate_settings'),
    path('history/', views.interview_history, name='candidate_history'),
    path('jobs/', views.job_board, name='candidate_job_board'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='candidate_apply_job'),
    path('delete_account/', views.delete_account, name='candidate_delete_account'),
    path('change_password/', views.change_password, name='candidate_change_password'),
    path('interview/<int:interview_id>/cancel/', views.cancel_interview, name='candidate_cancel_interview'),
    path('request-interview/', views.request_interview, name='candidate_request_interview'),
    path('request-interview/cancel/', views.cancel_request, name='candidate_cancel_request'),
    path('purchase-interview/', views.purchase_interview, name='candidate_purchase_interview'),
    path('purchase-interview/success/', views.purchase_interview_success, name='candidate_purchase_interview_success'),
    
    # AI Practice
    path('ai-practice/', views.ai_practice_list, name='candidate_ai_practice'),
    path('ai-practice/<int:session_id>/room/', views.ai_practice_room, name='candidate_ai_room'),
    path('ai-practice/<int:session_id>/api/', views.ai_practice_api, name='candidate_ai_api'),
]
