import os
import textwrap

templates_dir = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\emails'
os.makedirs(templates_dir, exist_ok=True)

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
    'welcome_candidate.html': get_base_template(
        'Welcome to TechPlus, {{ user.name }}!',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    We are thrilled to have you on board. TechPlus is the premier platform for technical talent to prove their skills and get hired by top companies.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    To get started, make sure to <strong>upload your resume</strong> and take a few free <strong>AI Practice Interviews</strong> to warm up!
</p>
<a href="{{ domain }}{% url 'candidate_dashboard' %}" class="btn">Go to Dashboard &rarr;</a>'''
    ),
    'application_received.html': get_base_template(
        'Application Received',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Hello {{ candidate.user.name }}, your application for <strong>{{ job.title }}</strong> at <strong>{{ job.company.company_name }}</strong> has been successfully received.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Our team will review your profile and assign an expert interviewer shortly. We will notify you via email when your interview is scheduled.
</p>
<a href="{{ domain }}{% url 'candidate_job_board' %}" class="btn">View My Applications &rarr;</a>'''
    ),
    'interview_results.html': get_base_template(
        'Your Interview Results are Ready',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Hello {{ candidate.user.name }}, your recent technical interview has been evaluated and your final TechPlus Score has been updated!
</p>
<div class="details-box">
    <div class="detail-row">
        <span class="detail-label">Score</span>
        <span class="detail-value" style="color: #10B981;">{{ score }}/100</span>
    </div>
</div>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Log in to view the detailed feedback from your interviewer.
</p>
<a href="{{ domain }}{% url 'candidate_dashboard' %}" class="btn">View Detailed Feedback &rarr;</a>'''
    ),
    'offer_received.html': get_base_template(
        'You have received a Job Offer!',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Congratulations {{ candidate.user.name }}! <strong>{{ company.company_name }}</strong> was highly impressed by your interview performance and has extended a formal job offer to you.
</p>
<div class="details-box">
    <div class="detail-row">
        <span class="detail-label">Company</span>
        <span class="detail-value">{{ company.company_name }}</span>
    </div>
    <div class="detail-row">
        <span class="detail-label">CTC / Salary</span>
        <span class="detail-value" style="color: #10B981;">₹{{ offer_amount }}</span>
    </div>
</div>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    The company has also included additional details and perks. Log in to review and respond to your offer.
</p>
<a href="{{ domain }}{% url 'candidate_dashboard' %}" class="btn">View Offer Details &rarr;</a>'''
    ),
    'account_approved_interviewer.html': get_base_template(
        'Your Interviewer Account is Approved',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Hello {{ user.name }}, your interviewer profile has been reviewed and successfully approved by the TechPlus administration team.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    You are now eligible to receive interview assignments. Ensure your profile is up to date and your availability is clear.
</p>
<a href="{{ domain }}{% url 'interviewer_dashboard' %}" class="btn">Go to Interviewer Dashboard &rarr;</a>'''
    ),
    'payout_processed.html': get_base_template(
        'Payout Processed Successfully',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Hello {{ user.name }}, your withdrawal request has been successfully processed and paid out.
</p>
<div class="details-box">
    <div class="detail-row">
        <span class="detail-label">Amount</span>
        <span class="detail-value" style="color: #10B981;">₹{{ amount }}</span>
    </div>
    <div class="detail-row">
        <span class="detail-label">Status</span>
        <span class="detail-value">PAID</span>
    </div>
</div>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    The funds should reflect in your account shortly. Thank you for your continued excellence in conducting interviews!
</p>
<a href="{{ domain }}{% url 'interviewer_dashboard' %}" class="btn">View Earnings &rarr;</a>'''
    ),
    'account_approved_company.html': get_base_template(
        'Your Company Account is Approved',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Hello {{ user.name }}, your company profile for <strong>{{ company.company_name }}</strong> has been verified by our team.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    You now have full access to the TechPlus Candidate Marketplace. You can browse pre-vetted candidates, view their scores and transcripts, and hire top talent instantly.
</p>
<a href="{{ domain }}{% url 'company_marketplace' %}" class="btn">Browse Candidate Marketplace &rarr;</a>'''
    ),
    'candidate_hired.html': get_base_template(
        'Candidate Hired - Invoice Generated',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    Congratulations on successfully hiring <strong>{{ candidate.user.name }}</strong>! 
</p>
<div class="details-box">
    <div class="detail-row">
        <span class="detail-label">Candidate</span>
        <span class="detail-value">{{ candidate.user.name }}</span>
    </div>
    <div class="detail-row">
        <span class="detail-label">Platform Fee</span>
        <span class="detail-value" style="color: #10B981;">₹{{ fee_amount }}</span>
    </div>
</div>
<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    As per our marketplace terms, the platform fee (equivalent to 1 month of the agreed salary) has been invoiced to your account.
</p>
<a href="{{ domain }}{% url 'company_dashboard' %}" class="btn">View Dashboard &rarr;</a>'''
    ),
    'admin_alert.html': get_base_template(
        'Admin Alert: Action Required',
        '''<p style="font-size: 16px; line-height: 1.7; color: #888888; margin-bottom: 32px;">
    A new action requires your attention in the TechPlus Management Portal.
</p>
<div class="details-box">
    <div class="detail-row">
        <span class="detail-label">Action Type</span>
        <span class="detail-value">{{ alert_type }}</span>
    </div>
    <div class="detail-row">
        <span class="detail-label">Details</span>
        <span class="detail-value">{{ alert_message }}</span>
    </div>
</div>
<a href="{{ domain }}{% url 'management_dashboard' %}" class="btn">Go to Management Portal &rarr;</a>'''
    )
}

for filename, content in emails.items():
    with open(os.path.join(templates_dir, filename), 'w', encoding='utf-8') as f:
        f.write(content)
