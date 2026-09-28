import os
import textwrap

templates_dir = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\emails'

def get_base_template(title, body_content):
    return textwrap.dedent(f"""\
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #000000; color: #888888; margin: 0; padding: 40px 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #050505; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #222222; }}
        .header {{ background-color: #000000; padding: 30px 24px; text-align: center; border-bottom: 1px solid #111111; position: relative; overflow: hidden; }}
        
        .logo {{ color: #ffffff; font-size: 28px; font-weight: 800; text-decoration: none; display: inline-block; letter-spacing: -0.5px; }}
        .logo-box {{ background-color: #ffffff; color: #000000; display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 16px; margin-right: 6px; vertical-align: middle; }}
        
        .content {{ padding: 40px; }}
        .title {{ font-size: 22px; font-weight: 700; margin-bottom: 24px; color: #ffffff; }}
        
        .details-box {{ background-color: #111111; border: 1px solid #222222; border-radius: 12px; padding: 24px; margin-bottom: 32px; }}
        .detail-row {{ margin-bottom: 16px; font-size: 15px; }}
        .detail-row:last-child {{ margin-bottom: 0; }}
        
        .detail-label {{ font-weight: 700; color: #666666; width: 120px; display: inline-block; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; }}
        .detail-value {{ font-weight: 600; color: #ffffff; font-size: 16px; }}
        
        .btn {{ display: inline-block; background-color: #ffffff; color: #000000; text-decoration: none; font-weight: 800; padding: 16px 28px; border-radius: 10px; text-align: center; width: 100%; box-sizing: border-box; font-size: 16px; transition: background-color 0.2s; }}
        
        .footer {{ padding: 24px; text-align: center; font-size: 13px; color: #444444; border-top: 1px solid #111111; background-color: #000000; }}
        
        .glow {{ position: absolute; top: -50px; left: 50%; transform: translateX(-50%); width: 200px; height: 100px; background: radial-gradient(circle, rgba(59,130,246,0.2) 0%, rgba(0,0,0,0) 70%); border-radius: 50%; pointer-events: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="glow"></div>
            <div class="logo">
                <div style="background-color: #ffffff; color: #000000; display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; margin-right: 10px; vertical-align: middle;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" fill="currentColor" style="width: 14px; height: 14px;"><path d="M264.5 5.2c14.9-6.9 32.1-6.9 47 0l218.6 101c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 149.8C37.4 145.9 32 137.4 32 128s5.4-17.9 13.9-21.8L264.5 5.2zM476.9 209.6l53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 277.8C37.4 273.9 32 265.4 32 256s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0l152-70.2zM476.9 337.6l53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 405.8C37.4 401.9 32 393.4 32 384s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0l152-70.2z"/></svg></div>TechPlus
            </div>
        </div>
        <div class="content">
            <div class="title">{title}</div>
            {body_content}
        </div>
        <div class="footer">
            &copy; {{% now "Y" %}} TechPlus. All rights reserved.<br>
            Secure Technical Hiring Platform.
        </div>
    </div>
</body>
</html>
""")

emails = {
    'welcome_company.html': get_base_template(
        'Welcome to TechPlus, {{ company.company_name }}!',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Thank you for registering on TechPlus. Your account is currently under review by our administration team.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Once approved, you will have access to the Candidate Marketplace to source, interview, and hire top-tier technical talent. We will send you an email as soon as your account is verified.
</p>
<a href="{{ domain }}{% url 'company_dashboard' %}" class="btn">Go to Dashboard &rarr;</a>'''
    ),
    'welcome_interviewer.html': get_base_template(
        'Welcome to TechPlus, {{ user.name }}!',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Thank you for applying to be an expert interviewer on TechPlus! Your application is currently under review by our administration team.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Once approved, you will start receiving interview assignments and can earn payouts for conducting technical evaluations. We will notify you via email as soon as your account is verified.
</p>
<a href="{{ domain }}{% url 'interviewer_dashboard' %}" class="btn">Go to Dashboard &rarr;</a>'''
    ),
    'payout_requested.html': get_base_template(
        'Payout Request Received',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Hello {{ user.name }}, we have received your payout request.
</p>
<div class="details-box">
    <div class="detail-row">
        <span class="detail-label">Amount</span>
        <span class="detail-value" style="color: #60A5FA;">₹{{ amount }}</span>
    </div>
    <div class="detail-row">
        <span class="detail-label">Status</span>
        <span class="detail-value">PENDING</span>
    </div>
</div>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Our team is processing your request. It typically takes 1-3 business days for the funds to reflect in your account. You will receive an email once it is processed.
</p>
<a href="{{ domain }}{% url 'interviewer_dashboard' %}" class="btn">View Payout Status &rarr;</a>'''
    ),
    'password_reset_success.html': get_base_template(
        'Password Reset Successfully',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Hello {{ user.name }}, your TechPlus account password has been successfully reset.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    If you did not make this change, please contact our support team immediately to secure your account.
</p>
<a href="{{ domain }}{% url 'login' %}" class="btn">Log in to your account &rarr;</a>'''
    ),
    'interview_rescheduled.html': get_base_template(
        'Interview Rescheduled',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Hello {{ user.name }}, your upcoming interview on TechPlus has been rescheduled.
</p>
<div class="details-box">
    <div class="detail-row">
        <span class="detail-label">New Date</span>
        <span class="detail-value" style="color: #60A5FA;">{{ new_date }}</span>
    </div>
    <div class="detail-row">
        <span class="detail-label">New Time</span>
        <span class="detail-value" style="color: #60A5FA;">{{ new_time }}</span>
    </div>
</div>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Please review your calendar and ensure you are available at the new time.
</p>
<a href="{{ domain }}{% url 'home' %}" class="btn">Go to Dashboard &rarr;</a>'''
    )
}

for filename, content in emails.items():
    with open(os.path.join(templates_dir, filename), 'w', encoding='utf-8') as f:
        f.write(content)
