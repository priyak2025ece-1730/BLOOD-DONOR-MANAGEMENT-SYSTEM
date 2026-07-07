import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bdms_project.settings')
django.setup()

from django.contrib.auth.models import User
from blood.models import DonorProfile, BloodRequest, BloodInventory

def populate():
    print("Clearing existing sample data to prevent duplicates...")
    DonorProfile.objects.all().delete()
    User.objects.exclude(username='admin').delete()
    BloodInventory.objects.all().delete()
    BloodRequest.objects.all().delete()

    print("Adding Blood Inventory...")
    BloodInventory.objects.create(blood_group='A+', units_available=10)
    BloodInventory.objects.create(blood_group='O+', units_available=15)
    BloodInventory.objects.create(blood_group='B-', units_available=3)
    BloodInventory.objects.create(blood_group='AB+', units_available=0)
    
    print("Adding Donors...")
    u1 = User.objects.create_user(username='johndoe', email='john@example.com', password='password123')
    DonorProfile.objects.create(
        user=u1, name='John Doe', blood_group='O+', contact_number='555-0101',
        age=28, gender='Male', location='New York', address='123 5th Ave, NY', is_available=True
    )
    
    u2 = User.objects.create_user(username='janedoe', email='jane@example.com', password='password123')
    DonorProfile.objects.create(
        user=u2, name='Jane Smith', blood_group='A+', contact_number='555-0202',
        age=32, gender='Female', location='Brooklyn', address='456 Flatbush Ave, Brooklyn, NY', is_available=True
    )

    u3 = User.objects.create_user(username='markz', email='mark@example.com', password='password123')
    DonorProfile.objects.create(
        user=u3, name='Mark Zuckerberg', blood_group='B-', contact_number='555-0303',
        age=39, gender='Male', location='Queens', address='789 Queens Blvd, NY', is_available=False
    )
    
    print("Adding Blood Requests...")
    BloodRequest.objects.create(
        requested_by=u1, patient_name='Alice Wonderland', blood_group='B-', location='Manhattan',
        hospital='Bellevue Hospital', units_required=2, status='Pending'
    )
    
    BloodRequest.objects.create(
        requested_by=u2, patient_name='Bob Builder', blood_group='O+', location='Brooklyn',
        hospital='Brooklyn Hospital Center', units_required=1, status='Approved'
    )
    
    print("Populated Database with Realistic Sample Data Successfully!")

if __name__ == '__main__':
    populate()
