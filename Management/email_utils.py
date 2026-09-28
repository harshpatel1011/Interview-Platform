import uuid
from datetime import timedelta, timezone as dt_timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

def generate_ics(interview, domain):
    """Generates an iCalendar (.ics) string for the given interview."""
    dt_format = "%Y%m%dT%H%M%SZ"
    
    # Convert to UTC for the ICS file
    start_time = interview.scheduled_time.astimezone(dt_timezone.utc)
    end_time = start_time + timedelta(hours=1)
    
    dtstart = start_time.strftime(dt_format)
    dtend = end_time.strftime(dt_format)
    dtstamp = timezone.now().astimezone(dt_timezone.utc).strftime(dt_format)
    
    event_uuid = str(uuid.uuid4())
    meeting_url = f"{domain}{interview.meeting_link}"
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//TechPlus//Interview Platform//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:{event_uuid}
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:TechPlus Interview: {interview.candidate.user.name}
DESCRIPTION:Join your technical interview here: {meeting_url}
URL:{meeting_url}
STATUS:CONFIRMED
ORGANIZER;CN="TechPlus":mailto:noreply@techplus.io
END:VEVENT
END:VCALENDAR"""

    return ics_content

def send_interview_invites(request, interview):
    """Sends HTML email with ICS attachment to candidate and interviewer."""
    
    # Get domain for absolute URLs
    domain = request.build_absolute_uri('/')[:-1]
    
    # Send to Candidate
    _send_single_invite(
        interview=interview, 
        recipient=interview.candidate.user, 
        domain=domain
    )
    
    # Send to Interviewer
    _send_single_invite(
        interview=interview, 
        recipient=interview.interviewer.user, 
        domain=domain
    )

def _send_single_invite(interview, recipient, domain):
    subject = f"Interview Scheduled: {interview.scheduled_time.strftime('%b %d, %Y')}"
    
    context = {
        'interview': interview,
        'recipient_name': recipient.name,
        'domain': domain,
    }
    
    # Render HTML content
    html_content = render_to_string('emails/interview_invite.html', context)
    text_content = f"Hello {recipient.name},\n\nYou have an interview scheduled on {interview.scheduled_time}.\n\nJoin link: {domain}{interview.meeting_link}"
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient.email]
    )
    
    # Attach HTML
    email.attach_alternative(html_content, "text/html")
    
    # Attach ICS Calendar File
    ics_content = generate_ics(interview, domain)
    email.attach(
        filename='invite.ics',
        content=ics_content,
        mimetype='text/calendar'
    )
    
    email.send(fail_silently=False)


def send_interview_update(request, interview, update_type):
    """Sends HTML email for COMPLETED or CANCELLED statuses."""
    domain = request.build_absolute_uri('/')[:-1]
    
    # Send to Candidate
    _send_update_single(
        interview=interview, 
        recipient=interview.candidate.user, 
        domain=domain,
        update_type=update_type
    )
    
    # Send to Interviewer
    _send_update_single(
        interview=interview, 
        recipient=interview.interviewer.user, 
        domain=domain,
        update_type=update_type
    )

def _send_update_single(interview, recipient, domain, update_type):
    if update_type == 'CANCELLED':
        subject = f"Interview Cancelled: {interview.candidate.user.name}"
        template_name = 'emails/interview_cancelled.html'
    elif update_type == 'COMPLETED':
        subject = f"Interview Completed: {interview.candidate.user.name}"
        template_name = 'emails/interview_completed.html'
    else:
        return
        
    context = {
        'interview': interview,
        'recipient_name': recipient.name,
        'domain': domain,
    }
    
    html_content = render_to_string(template_name, context)
    text_content = f"Hello {recipient.name},\n\nYour interview status has been updated to {update_type}."
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient.email]
    )
    
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
