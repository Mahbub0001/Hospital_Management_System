from django.contrib import admin
from .models import Patient, Doctor, Appointment, Department, MedicalRecord, Prescription, Billing

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'blood_type']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['blood_type', 'gender']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'specialization', 'email', 'phone']
    search_fields = ['first_name', 'last_name', 'specialization']
    list_filter = ['specialization', 'department']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'time', 'status']
    search_fields = ['patient__first_name', 'doctor__first_name']
    list_filter = ['status', 'date']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head_of_department']
    search_fields = ['name']

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'diagnosis', 'created_at']
    search_fields = ['patient__first_name', 'diagnosis']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'medication', 'dosage', 'created_at']
    search_fields = ['patient__first_name', 'medication']

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['patient', 'amount', 'status', 'created_at']
    search_fields = ['patient__first_name']
    list_filter = ['status']
