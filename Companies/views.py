import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from Candidates.models import CandidateProfile
from .models import CompanyProfile, UnlockTransaction

from django.contrib.auth import login
from .forms import CompanyRegistrationForm

def register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'COMPANY'
            user.save()
            
            profile = CompanyProfile.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name']
            )
            
            from Core.email_manager import send_welcome_company
            send_welcome_company(profile)
            
            login(request, user)
            return redirect('company_dashboard')
    else:
        form = CompanyRegistrationForm()
        
    return render(request, 'companies/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.role != 'COMPANY':
        return redirect('home')
    
    company = request.user.company_profile
    unlocked_transactions = UnlockTransaction.objects.filter(company=company, status='SUCCESS').select_related('candidate', 'candidate__user')
    job_posts = company.job_posts.all().order_by('-created_at')
    
    if request.method == 'POST' and company.is_verified:
        form_type = request.POST.get('form_type')
        
        if form_type == 'job_post':
            from .models import JobPost
            title = request.POST.get('title')
            description = request.POST.get('description')
            skills = request.POST.get('skills')
            if title and description:
                JobPost.objects.create(
                    company=company,
                    title=title,
                    description=description,
                    required_skills=skills
                )
                messages.success(request, 'Job post created successfully.')
        
        elif form_type == 'interview_request':
            # Create a mock or real request to Management
            candidate_email = request.POST.get('candidate_email')
            role = request.POST.get('role')
            messages.success(request, f'Interview request for {candidate_email} ({role}) sent to Management team!')
            
        elif form_type == 'update_outcome':
            txn_id = request.POST.get('transaction_id')
            new_outcome = request.POST.get('outcome')
            txn = get_object_or_404(UnlockTransaction, id=txn_id, company=company)
            txn.outcome = new_outcome
            txn.save()
            
            # Update global candidate status
            if new_outcome == 'HIRED':
                candidate = txn.candidate
                candidate.status = 'HIRED'
                candidate.save()
            elif new_outcome == 'OFFERED':
                candidate = txn.candidate
                if candidate.status not in ['HIRED']:
                    candidate.status = 'OFFERED'
                    candidate.save()
            elif new_outcome == 'REJECTED':
                candidate = txn.candidate
                # Don't let a rejection override an existing hire or offer
                if candidate.status not in ['HIRED', 'OFFERED']:
                    candidate.status = 'REJECTED'
                    candidate.save()
            
            messages.success(request, f"Updated candidate status to {new_outcome}.")
            
        return redirect('company_dashboard')
    
    return render(request, 'companies/dashboard.html', {
        'company': company,
        'unlocked_transactions': unlocked_transactions,
        'job_posts': job_posts
    })

@login_required
def marketplace(request):
    if request.user.role != 'COMPANY':
        return redirect('home')
        
    company = request.user.company_profile
    if not company.is_verified:
        messages.warning(request, "Your account must be verified by an admin before you can access the marketplace.")
        return redirect('company_dashboard')
    
    # Get all candidates who have been interviewed (have a score)
    # Exclude those the company has already unlocked
    unlocked_candidate_ids = UnlockTransaction.objects.filter(company=company, status='SUCCESS').values_list('candidate_id', flat=True)
    candidates = CandidateProfile.objects.exclude(score=None).exclude(id__in=unlocked_candidate_ids).order_by('-score')
    
    # Filtering logic
    designation = request.GET.get('designation')
    min_score = request.GET.get('min_score')
    
    if designation:
        candidates = candidates.filter(designations__icontains=designation)
    if min_score and min_score.isdigit():
        candidates = candidates.filter(score__gte=int(min_score))
        
    return render(request, 'companies/marketplace.html', {
        'candidates': candidates,
    })

@login_required
def extend_offer(request, transaction_id):
    if request.user.role != 'COMPANY':
        return redirect('home')
        
    company = request.user.company_profile
    txn = get_object_or_404(UnlockTransaction, id=transaction_id, company=company)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        details = request.POST.get('details')
        if amount:
            txn.offer_amount = amount
            txn.offer_details = details
            txn.outcome = 'OFFERED'
            txn.save()
            
            candidate = txn.candidate
            if candidate.status not in ['HIRED']:
                candidate.status = 'OFFERED'
                candidate.save()
                
            from Core.email_manager import send_offer_received
            send_offer_received(candidate, company, amount)
                
            messages.success(request, f"Offer of ₹{amount} extended to {candidate.user.name}!")
            return redirect('company_dashboard')
            
    return render(request, 'companies/extend_offer.html', {'txn': txn})

@login_required
def hire_candidate(request, transaction_id):
    if request.user.role != 'COMPANY':
        return redirect('home')
        
    company = request.user.company_profile
    txn = get_object_or_404(UnlockTransaction, id=transaction_id, company=company)
    
    if request.method == 'POST':
        ctc_amount_str = request.POST.get('ctc_amount')
        
        if ctc_amount_str:
            try:
                ctc_amount = float(ctc_amount_str)
                monthly_fee = ctc_amount / 12.0
                
                txn.offer_amount = ctc_amount  # Save CTC in offer_amount
                txn.amount = monthly_fee       # Platform fee is 1 month salary
                txn.outcome = 'HIRED'
                txn.save()
                
                candidate = txn.candidate
                candidate.status = 'HIRED'
                candidate.save()
                    
                from Core.email_manager import send_candidate_hired
                send_candidate_hired(candidate, company, monthly_fee)
                
                messages.success(request, f"Candidate {candidate.user.name} marked as HIRED! A platform fee of ₹{monthly_fee:.2f} (1 month salary) has been invoiced.")
                return redirect('company_dashboard')
            except ValueError:
                messages.error(request, "Invalid CTC amount provided.")
            
    return render(request, 'companies/hire_candidate.html', {'txn': txn})

@login_required
def unlock_candidate(request, candidate_id):
    if request.user.role != 'COMPANY':
        return redirect('home')
        
    company = request.user.company_profile
    candidate = get_object_or_404(CandidateProfile, id=candidate_id)
    
    # Check if already unlocked
    if UnlockTransaction.objects.filter(company=company, candidate=candidate, status='SUCCESS').exists():
        messages.info(request, "You have already unlocked this candidate.")
        return redirect('company_dashboard')
        
    if request.method == 'POST':
        transaction, created = UnlockTransaction.objects.get_or_create(
            company=company, candidate=candidate,
            defaults={'amount': 0.00}
        )
        
        transaction.status = 'SUCCESS'
        transaction.razorpay_payment_id = 'FREE_UNLOCK'
        transaction.save()
        
        messages.success(request, f"Successfully unlocked {candidate.user.name}'s profile for free!")
        return redirect('company_dashboard')
            
    return render(request, 'companies/unlock_confirm.html', {'candidate': candidate})

@login_required
def payment_callback(request):
    if request.method == "POST":
        company = request.user.company_profile
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')
        
        transaction = get_object_or_404(UnlockTransaction, razorpay_order_id=razorpay_order_id)
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            # Verify signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            
            # Payment successful
            transaction.status = 'SUCCESS'
            transaction.razorpay_payment_id = razorpay_payment_id
            transaction.razorpay_signature = razorpay_signature
            transaction.save()
            
            messages.success(request, f"Successfully unlocked {transaction.candidate.user.name}'s profile!")
            return redirect('company_dashboard')
            
        except razorpay.errors.SignatureVerificationError:
            transaction.status = 'FAILED'
            transaction.save()
            messages.error(request, "Payment verification failed. Please try again.")
            return redirect('company_marketplace')
            
    return redirect('home')
@login_required
def candidate_detail(request, candidate_id):
    if request.user.role != 'COMPANY':
        return redirect('home')
        
    company = request.user.company_profile
    candidate = get_object_or_404(CandidateProfile, id=candidate_id)
    
    # Check if company has unlocked this candidate
    is_unlocked = UnlockTransaction.objects.filter(company=company, candidate=candidate, status='SUCCESS').exists()
    
    return render(request, 'companies/candidate_detail.html', {
        'candidate': candidate,
        'is_unlocked': is_unlocked
    })

@login_required
def profile(request):
    if request.user.role != 'COMPANY':
        return redirect('home')
    return render(request, 'companies/profile.html', {'company': request.user.company_profile})

@login_required
def profile_edit(request):
    if request.user.role != 'COMPANY':
        return redirect('home')
        
    company = request.user.company_profile
    from .forms import CompanyProfileEditForm
    
    if request.method == 'POST':
        form = CompanyProfileEditForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('company_profile')
    else:
        form = CompanyProfileEditForm(instance=company)
        
    return render(request, 'companies/profile_edit.html', {'form': form, 'company': company})
