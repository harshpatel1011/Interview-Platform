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
