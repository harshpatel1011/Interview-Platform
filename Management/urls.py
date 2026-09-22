from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='management_dashboard'),
    path('assign/<int:candidate_id>/', views.assign_interviewer, name='management_assign'),
]
