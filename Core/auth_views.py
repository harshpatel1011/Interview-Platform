from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import random
from datetime import timedelta
from Management.models import CustomUser

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            
            # Generate 6 digit OTP
            otp = str(random.randint(100000, 999999))
            user.reset_otp = otp
            user.reset_otp_expires_at = timezone.now() + timedelta(minutes=10)
            user.save()
            
            # Send Email
            from django.core.mail import EmailMultiAlternatives
            from django.template.loader import render_to_string
            
            subject = "TechPlus Password Reset Code"
            text_content = f"Hello {user.name},\n\nYour 6-digit OTP for password reset is: {otp}\nThis OTP is valid for 10 minutes.\n\nThank you."
            html_content = render_to_string('emails/otp_reset.html', {'user_name': user.name, 'otp': otp})
            
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            request.session['reset_email'] = email
            messages.success(request, f"An OTP has been sent to {email}")
            return redirect('password_reset_verify')
            
        except CustomUser.DoesNotExist:
            # Show error if email doesn't exist (user requested to not use anti-enumeration)
            messages.error(request, f"No account found with the email {email}.")
            return render(request, 'registration/password_reset_form.html')
            
    return render(request, 'registration/password_reset_form.html')

def password_reset_verify(request):
    email = request.session.get('reset_email')
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        input_email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=input_email)
            if user.reset_otp == otp and user.reset_otp_expires_at > timezone.now():
                # OTP is correct
                request.session['verified_email'] = input_email
                messages.success(request, "OTP verified successfully. Please enter your new password.")
                return redirect('password_reset_confirm')
            else:
                messages.error(request, "Invalid or expired OTP.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid or expired OTP.")
            
    return render(request, 'registration/password_reset_verify.html', {'email': email})

def password_reset_confirm(request):
    email = request.session.get('verified_email')
    if not email:
        return redirect('password_reset_request')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password == password_confirm:
            user = CustomUser.objects.get(email=email)
            user.set_password(password)
            user.reset_otp = None
            user.reset_otp_expires_at = None
            user.save()
            
            # Clear session
            del request.session['verified_email']
            if 'reset_email' in request.session:
                del request.session['reset_email']
                
            # Send password reset success email
            from Core.email_manager import send_html_email
            send_html_email(
                "Password Reset Successfully",
                "emails/password_reset_success.html",
                {'user': user},
                [user.email]
            )
                
            messages.success(request, "Your password has been successfully reset. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            
    return render(request, 'registration/password_reset_confirm.html')
