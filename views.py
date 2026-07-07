from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import DonorProfile, BloodRequest, BloodInventory, Notification
from .forms import UserSignUpForm, DonorRegistrationForm, BloodRequestForm

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    return render(request, 'contact.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Please register as a donor if you wish to donate.')
            return redirect('donor_register')
    else:
        form = UserSignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def donor_register(request):
    try:
        profile = request.user.donorprofile
        messages.info(request, "You are already registered as a donor.")
        return redirect('home')
    except DonorProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            messages.success(request, 'You have been successfully registered as a donor!')
            return redirect('donor_list')
    else:
        form = DonorRegistrationForm()
    return render(request, 'donor_register.html', {'form': form})

def donor_list(request):
    donors = DonorProfile.objects.filter(is_available=True)
    return render(request, 'donor_list.html', {'donors': donors})

def search_blood(request):
    query = False
    donors = DonorProfile.objects.filter(is_available=True)
    
    blood_group = request.GET.get('blood_group')
    location = request.GET.get('location')
    
    if blood_group or location:
        query = True
        if blood_group:
            donors = donors.filter(blood_group=blood_group)
        if location:
            donors = donors.filter(location__icontains=location)
            
    return render(request, 'search.html', {'donors': donors, 'query': query})

@login_required
def request_blood(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.requested_by = request.user
            req.save()
            
            matching_donors = DonorProfile.objects.filter(blood_group=req.blood_group, is_available=True).exclude(user=request.user)
            notifications_to_create = []
            for donor in matching_donors:
                if donor.user:
                    notifications_to_create.append(Notification(
                        user=donor.user,
                        message=f"EMERGENCY: Urgent requirement for {req.blood_group} blood at {req.hospital}, {req.location}. Please help save a life!",
                        notification_type='Emergency'
                    ))
            Notification.objects.bulk_create(notifications_to_create)

            messages.success(request, 'Blood request submitted successfully. We will review it shortly.')
            return redirect('home')
    else:
        form = BloodRequestForm()
    return render(request, 'request_blood.html', {'form': form})

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_donors = DonorProfile.objects.count()
    pending_requests = BloodRequest.objects.filter(status='Pending').count()
    approved_requests = BloodRequest.objects.filter(status='Approved').count()
    total_users = User.objects.count()
    
    recent_requests = BloodRequest.objects.all().order_by('-date_requested')[:10]
    inventory = BloodInventory.get_stock()
    
    context = {
        'total_donors': total_donors,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'total_users': total_users,
        'requests': recent_requests,
        'inventory': inventory,
    }
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(is_admin)
def update_request_status(request, req_id):
    if request.method == 'POST':
        req = get_object_or_404(BloodRequest, id=req_id)
        new_status = request.POST.get('status')
        if new_status in ['Approved', 'Rejected']:
            req.status = new_status
            req.save()
            
            # If approved, theoretically we should deduct from inventory if it exists
            # Let's add basic logic for it if inventory has it, if not, we can just approve
            if new_status == 'Approved':
                inv, created = BloodInventory.objects.get_or_create(blood_group=req.blood_group)
                if inv.units_available >= req.units_required:
                    inv.units_available -= req.units_required
                    inv.save()
                    messages.success(request, f'Request Approved. Deducted {req.units_required} units.')
                else:
                    messages.warning(request, f'Request Approved, but not enough units in inventory for {req.blood_group}.')
                
                if req.requested_by:
                    Notification.objects.create(
                        user=req.requested_by,
                        message=f"Good news! Your blood request at {req.hospital} has been APPROVED.",
                        notification_type='Availability'
                    )
            else:
                messages.error(request, 'Request Rejected.')
                if req.requested_by:
                    Notification.objects.create(
                        user=req.requested_by,
                        message=f"Unfortunately, your blood request at {req.hospital} has been REJECTED.",
                        notification_type='System'
                    )
                
    return redirect('admin_dashboard')

@login_required
def notifications_view(request):
    notifications_list = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications_list': notifications_list})

@login_required
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications')
