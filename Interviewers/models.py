from django.db import models
from django.conf import settings
from Candidates.models import CandidateProfile

class InterviewerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interviewer_profile')
    department = models.CharField(max_length=100, blank=True, null=True)
    
    # Track Interviewer Earnings
    earnings_per_interview = models.DecimalField(max_digits=8, decimal_places=2, default=200.00) # Rs 200 per interview
    
    # Track verified status
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Interviewer: {self.user.name}"
        
    @property
    def upcoming_interviews_count(self):
        return self.assigned_interviews.filter(status='SCHEDULED').count()
        
    @property
    def completed_interviews_count(self):
        return self.assigned_interviews.filter(status='COMPLETED').count()
        
    @property
    def total_earnings(self):
        return self.completed_interviews_count * self.earnings_per_interview

    @property
    def withdrawn_amount(self):
        from django.db.models import Sum
        withdrawn = self.withdrawals.filter(status__in=['PAID', 'APPROVED']).aggregate(Sum('amount'))['amount__sum']
        return withdrawn or 0
        
    @property
    def pending_withdrawal_amount(self):
        from django.db.models import Sum
        pending = self.withdrawals.filter(status='PENDING').aggregate(Sum('amount'))['amount__sum']
        return pending or 0
        
    @property
    def available_balance(self):
        return float(self.total_earnings) - float(self.withdrawn_amount) - float(self.pending_withdrawal_amount)


class WithdrawalRequest(models.Model):
    interviewer = models.ForeignKey(InterviewerProfile, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_details = models.TextField(help_text="UPI ID or Bank Account details")
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
        ('REJECTED', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True, help_text="Admin notes, e.g., rejection reason or transaction ID")

    def __str__(self):
        return f"Withdrawal - {self.interviewer.user.name} - Rs {self.amount}"

class Interview(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(InterviewerProfile, on_delete=models.CASCADE, related_name='assigned_interviews')
    designation = models.CharField(max_length=255, default="Unspecified", help_text="The role/designation this interview is for")
    scheduled_time = models.DateTimeField()
    meeting_link = models.URLField(max_length=500, blank=True, null=True)
    
    # Detailed Grading Matrix (Max 100 points total)
    technical_score = models.IntegerField(null=True, blank=True, help_text="Out of 40")
    problem_solving_score = models.IntegerField(null=True, blank=True, help_text="Out of 25")
    communication_score = models.IntegerField(null=True, blank=True, help_text="Out of 15")
    culture_fit_score = models.IntegerField(null=True, blank=True, help_text="Out of 10")
    confidence_score = models.IntegerField(null=True, blank=True, help_text="Out of 10")
    
    # Overall calculated score & grade
    score = models.IntegerField(null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True, null=True)
    feedback = models.TextField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Auto-calculate the overall score sum if all matrix scores exist
        if all(v is not None for v in [self.technical_score, self.problem_solving_score, self.communication_score, self.culture_fit_score, self.confidence_score]):
            self.score = self.technical_score + self.problem_solving_score + self.communication_score + self.culture_fit_score + self.confidence_score
            
            # Auto-assign Grade
            if self.score >= 85:
                self.grade = "Excellent"
            elif self.score >= 65:
                self.grade = "Good"
            elif self.score >= 40:
                self.grade = "Average"
            else:
                self.grade = "Needs Improvement"
                
        super().save(*args, **kwargs)
    
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')

    def __str__(self):
        return f"Interview: {self.candidate.user.name} with {self.interviewer.user.name}"
