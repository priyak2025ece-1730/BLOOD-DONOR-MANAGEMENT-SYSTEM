from django.db import models
from django.contrib.auth.models import User

class BloodGroup(models.TextChoices):
    A_POS = 'A+', 'A+'
    A_NEG = 'A-', 'A-'
    B_POS = 'B+', 'B+'
    B_NEG = 'B-', 'B-'
    O_POS = 'O+', 'O+'
    O_NEG = 'O-', 'O-'
    AB_POS = 'AB+', 'AB+'
    AB_NEG = 'AB-', 'AB-'

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices)
    contact_number = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    location = models.CharField(max_length=100)
    address = models.TextField()
    is_available = models.BooleanField(default=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.blood_group}"


class BloodRequest(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'
        
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices)
    location = models.CharField(max_length=100)
    hospital = models.CharField(max_length=200)
    units_required = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=RequestStatus.choices, default=RequestStatus.PENDING)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.patient_name} - {self.blood_group}"

class BloodInventory(models.Model):
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices, unique=True)
    units_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.blood_group} - {self.units_available} Units"
    
    @classmethod
    def get_stock(cls):
        stock = {bg[0]: 0 for bg in BloodGroup.choices}
        for item in cls.objects.all():
            stock[item.blood_group] = item.units_available
        return stock

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[('Emergency', 'Emergency'), ('Availability', 'Availability'), ('System', 'System')], default='System')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} - {self.message[:20]}"
