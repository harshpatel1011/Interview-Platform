import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def send_html_email(subject, template_name, context, recipient_list):
    """
    Helper function to send HTML emails asynchronously.
    """
    context['domain'] = getattr(settings, 'DOMAIN_URL', 'http://127.0.0.1:8000') # Ensure domain is available
    
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list
    )
    email.attach_alternative(html_content, "text/html")
    
    # Send asynchronously to not block the view response
    class EmailThread(threading.Thread):
        def run(self):
            try:
                email.send()
            except Exception as e:
                print(f"Failed to send email {subject}: {e}")
                
    EmailThread().start()


def send_welcome_candidate(user):
    send_html_email(
        "Welcome to TechPlus!",
        "emails/welcome_candidate.html",
        {'user': user},
        [user.email]
    )

def send_application_received(candidate, job):
    send_html_email(
        f"Application Received: {job.title}",
        "emails/application_received.html",
        {'candidate': candidate, 'job': job},
        [candidate.user.email]
    )

def send_interview_results(candidate, score):
    send_html_email(
        "Your Interview Results are Ready",
        "emails/interview_results.html",
        {'candidate': candidate, 'score': score},
        [candidate.user.email]
    )

def send_offer_received(candidate, company, offer_amount):
    send_html_email(
        "You have received a Job Offer!",
        "emails/offer_received.html",
        {'candidate': candidate, 'company': company, 'offer_amount': offer_amount},
        [candidate.user.email]
    )

def send_welcome_company(company_profile):
    send_html_email(
        "Welcome to TechPlus!",
        "emails/welcome_company.html",
        {'company': company_profile},
        [company_profile.user.email]
    )

def send_welcome_interviewer(user):
    send_html_email(
        "Welcome to TechPlus!",
        "emails/welcome_interviewer.html",
        {'user': user},
        [user.email]
    )

def send_account_approved(user):
    if user.role == 'COMPANY':
        template = "emails/account_approved_company.html"
    elif user.role == 'INTERVIEWER':
        template = "emails/account_approved_interviewer.html"
    else:
        return
        
    send_html_email(
        "Your Account is Approved",
        template,
        {'user': user, 'company': getattr(user, 'company_profile', None)},
        [user.email]
    )

def send_candidate_hired(candidate, company_profile, fee_amount):
    send_html_email(
        "Candidate Hired - Invoice Generated",
        "emails/candidate_hired.html",
        {'candidate': candidate, 'fee_amount': fee_amount},
        [company_profile.user.email]
    )

def send_payout_requested(user, amount):
    send_html_email(
        "Payout Request Received",
        "emails/payout_requested.html",
        {'user': user, 'amount': amount},
        [user.email]
    )

def send_payout_processed(user, amount):
    send_html_email(
        "Payout Processed Successfully",
        "emails/payout_processed.html",
        {'user': user, 'amount': amount},
        [user.email]
    )

def send_admin_alert(alert_type, alert_message):
    # Sends to all superusers
    admin_emails = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
    if not admin_emails:
        return
        
    send_html_email(
        f"Admin Alert: {alert_type}",
        "emails/admin_alert.html",
        {'alert_type': alert_type, 'alert_message': alert_message},
        admin_emails
    )
