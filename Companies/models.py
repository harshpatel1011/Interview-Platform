from django.db import models
from django.conf import settings
from Candidates.models import CandidateProfile

class CompanyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    # Track verified status (Admin can verify companies)
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class UnlockTransaction(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='unlocked_candidates')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='unlocked_by_companies')
    
    # Razorpay Payment Details
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=500.00) # cost to unlock
    status = models.CharField(max_length=20, default='PENDING', choices=(
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    ))
    
    OUTCOME_CHOICES = (
        ('EVALUATING', 'Evaluating'),
        ('OFFERED', 'Offered'),
        ('HIRED', 'Hired'),
        ('REJECTED', 'Rejected'),
    )
    outcome = models.CharField(max_length=20, default='EVALUATING', choices=OUTCOME_CHOICES)
    
    offer_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Offer CTC in INR")
    offer_details = models.TextField(null=True, blank=True)
    
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'candidate')

    def __str__(self):
        return f"{self.company.company_name} unlocked {self.candidate.user.name}"

class JobPost(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.CharField(max_length=500, help_text="Comma separated skills")
    min_experience = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} at {self.company.company_name}"

class InterviewRequest(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='interview_requests')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='interview_requests')
    job_post = models.ForeignKey(JobPost, on_delete=models.SET_NULL, null=True, blank=True)
    
    REQUESTER_CHOICES = (
        ('COMPANY', 'Company requested Candidate'),
        ('CANDIDATE', 'Candidate applied to Company')
    )
    requester = models.CharField(max_length=20, choices=REQUESTER_CHOICES)
    
    status = models.CharField(max_length=20, default='PENDING', choices=(
        ('PENDING', 'Pending Admin Approval'),
        ('APPROVED', 'Approved (Scheduled)'),
        ('REJECTED', 'Rejected')
    ))
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_requester_display()} - {self.status}"
 
 
