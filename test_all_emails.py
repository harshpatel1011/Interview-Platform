import os
import sys
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
django.setup()

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# ==========================================
# ENTER THE EMAIL ADDRESS YOU WANT TO SEND TO
# ==========================================
TARGET_EMAIL = input("Enter the email address to receive test emails: ")

if not TARGET_EMAIL:
    print("No email provided. Exiting.")
    sys.exit()

def send_test_email(subject, template_name, context):
    context['domain'] = getattr(settings, 'DOMAIN_URL', 'http://127.0.0.1:8000')
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[TARGET_EMAIL]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    print(f"✅ Sent: {template_name}")

class MockObj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

# Mock Data
user = MockObj(name="Harsh Patel", email=TARGET_EMAIL)
company = MockObj(company_name="Google", user=user)
candidate = MockObj(user=user)
job = MockObj(title="Senior Django Developer", company=company)
import datetime
interview = MockObj(candidate=candidate, interviewer=MockObj(user=MockObj(name="Senior Expert")), scheduled_time=datetime.datetime.now(), meeting_link="/room/1234")

emails_to_test = [
    {
        "subject": "Welcome Candidate",
        "template": "emails/welcome_candidate.html",
        "context": {'user': user}
    },
    {
        "subject": "Welcome Company",
        "template": "emails/welcome_company.html",
        "context": {'company': company}
    },
    {
        "subject": "Welcome Interviewer",
        "template": "emails/welcome_interviewer.html",
        "context": {'user': user}
    },
    {
        "subject": "Application Received",
        "template": "emails/application_received.html",
        "context": {'candidate': candidate, 'job': job}
    },
    {
        "subject": "Interview Results",
        "template": "emails/interview_results.html",
        "context": {'candidate': candidate, 'score': 95}
    },
    {
        "subject": "Offer Received",
        "template": "emails/offer_received.html",
        "context": {'candidate': candidate, 'company': company, 'offer_amount': '15,00,000'}
    },
    {
        "subject": "Account Approved (Interviewer)",
        "template": "emails/account_approved_interviewer.html",
        "context": {'user': user}
    },
    {
        "subject": "Account Approved (Company)",
        "template": "emails/account_approved_company.html",
        "context": {'user': user, 'company': company}
    },
    {
        "subject": "Candidate Hired - Invoice",
        "template": "emails/candidate_hired.html",
        "context": {'candidate': candidate, 'fee_amount': '1,25,000'}
    },
    {
        "subject": "Payout Requested",
        "template": "emails/payout_requested.html",
        "context": {'user': user, 'amount': '2,500'}
    },
    {
        "subject": "Payout Processed",
        "template": "emails/payout_processed.html",
        "context": {'user': user, 'amount': '2,500'}
    },
    {
        "subject": "Admin Alert",
        "template": "emails/admin_alert.html",
        "context": {'alert_type': 'New Company Registration', 'alert_message': 'Company Google has registered and awaits verification.'}
    },
    {
        "subject": "Password Reset Success",
        "template": "emails/password_reset_success.html",
        "context": {'user': user}
    },
    {
        "subject": "Interview Rescheduled",
        "template": "emails/interview_rescheduled.html",
        "context": {'user': user, 'new_date': 'October 15, 2026', 'new_time': '10:00 AM IST'}
    },
    {
        "subject": "OTP Password Reset",
        "template": "emails/otp_reset.html",
        "context": {'user_name': 'Harsh Patel', 'otp': '123456'}
    },
    {
        "subject": "Interview Invite",
        "template": "emails/interview_invite.html",
        "context": {'recipient_name': 'Harsh Patel', 'interview': interview}
    },
    {
        "subject": "Interview Cancelled",
        "template": "emails/interview_cancelled.html",
        "context": {'recipient_name': 'Harsh Patel', 'interview': interview}
    },
    {
        "subject": "Interview Completed",
        "template": "emails/interview_completed.html",
        "context": {'recipient_name': 'Harsh Patel', 'interview': interview}
    }
]

print(f"Sending {len(emails_to_test)} test emails to {TARGET_EMAIL}...")
for email in emails_to_test:
    try:
        send_test_email(email['subject'], email['template'], email['context'])
    except Exception as e:
        print(f"❌ Failed to send {email['template']}: {str(e)}")

print("\nAll done! Check your inbox.")
