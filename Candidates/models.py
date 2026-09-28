from django.db import models
from django.conf import settings

class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate_profile')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    designations = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated list of applied designations")
    applied_date = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = (
        ('PENDING', 'Applied'),
        ('ASSIGNED', 'Interviewing'),
        ('INTERVIEWED', 'Evaluated'),
        ('OFFERED', 'Offered'),
        ('HIRED', 'Hired'),
        ('REJECTED', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name}'s Profile"
        
    @property
    def latest_interview(self):
        return self.interviews.order_by('-scheduled_time').first()

class AIPracticeSession(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='ai_sessions')
    designation = models.CharField(max_length=255, default="General Software Engineer")
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Financial
    is_free = models.BooleanField(default=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Results
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    transcript = models.TextField(blank=True, null=True, help_text="JSON dump of the chat history")
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"AI Practice: {self.candidate.user.name} ({self.get_status_display()})"
