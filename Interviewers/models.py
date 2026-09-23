from django.db import models
from django.conf import settings
from Candidates.models import CandidateProfile

class InterviewerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interviewer_profile')
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Interviewer: {self.user.name}"
        
    @property
    def upcoming_interviews_count(self):
        return self.assigned_interviews.filter(status='SCHEDULED').count()
        
    @property
    def completed_interviews_count(self):
        return self.assigned_interviews.filter(status='COMPLETED').count()

class Interview(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(InterviewerProfile, on_delete=models.CASCADE, related_name='assigned_interviews')
    designation = models.CharField(max_length=255, default="Unspecified", help_text="The role/designation this interview is for")
    scheduled_time = models.DateTimeField()
    meeting_link = models.URLField(max_length=500, blank=True, null=True)
    
    # We could store score here or on the candidate profile. Storing it here allows multiple interviews per candidate.
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')

    def __str__(self):
        return f"Interview: {self.candidate.user.name} with {self.interviewer.user.name}"
