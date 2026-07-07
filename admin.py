from django.contrib import admin
from .models import DonorProfile, BloodRequest, BloodInventory

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'contact_number', 'location', 'is_available')
    list_filter = ('blood_group', 'is_available', 'location')
    search_fields = ('name', 'location')

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'hospital', 'units_required', 'status', 'date_requested')
    list_filter = ('status', 'blood_group')
    search_fields = ('patient_name', 'hospital')

@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'units_available')
    list_filter = ('blood_group',)
