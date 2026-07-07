from django.test import TestCase
from django.contrib.auth.models import User
from .models import DonorProfile, BloodRequest, BloodInventory, Notification

class BloodModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        
    def test_donor_profile_creation(self):
        donor = DonorProfile.objects.create(
            user=self.user,
            name='Test Donor',
            blood_group='O+',
            contact_number='1234567890',
            age=25,
            gender='Male',
            location='New York',
            address='123 Test St',
            is_available=True
        )
        self.assertEqual(donor.name, 'Test Donor')
        self.assertEqual(donor.blood_group, 'O+')
        self.assertEqual(str(donor), 'Test Donor - O+')
        self.assertTrue(donor.is_available)

    def test_blood_request_creation(self):
        request = BloodRequest.objects.create(
            requested_by=self.user,
            patient_name='Test Patient',
            blood_group='A+',
            location='Los Angeles',
            hospital='City Hospital',
            units_required=2
        )
        self.assertEqual(request.patient_name, 'Test Patient')
        self.assertEqual(request.status, 'Pending')
        self.assertEqual(str(request), 'Request for Test Patient - A+')

    def test_blood_inventory_update(self):
        inventory = BloodInventory.objects.create(
            blood_group='B+',
            units_available=10
        )
        self.assertEqual(inventory.units_available, 10)
        self.assertEqual(str(inventory), 'B+ - 10 Units')
        
        stock = BloodInventory.get_stock()
        self.assertEqual(stock['B+'], 10)

    def test_notification_creation(self):
        notification = Notification.objects.create(
            user=self.user,
            message='Test emergency notification',
            notification_type='Emergency'
        )
        self.assertEqual(notification.notification_type, 'Emergency')
        self.assertFalse(notification.is_read)
        self.assertTrue(str(notification).startswith('Emergency - Test emergency'))
