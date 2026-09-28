from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='company_register'),
    path('dashboard/', views.dashboard, name='company_dashboard'),
    path('marketplace/', views.marketplace, name='company_marketplace'),
    path('unlock/<int:candidate_id>/', views.unlock_candidate, name='company_unlock'),
    path('transaction/<int:transaction_id>/offer/', views.extend_offer, name='company_extend_offer'),
    path('transaction/<int:transaction_id>/hire/', views.hire_candidate, name='company_hire_candidate'),
    path('candidate/<int:candidate_id>/', views.candidate_detail, name='company_candidate_detail'),
    path('payment/callback/', views.payment_callback, name='company_payment_callback'),
]
