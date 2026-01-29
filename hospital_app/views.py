from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from datetime import datetime, date, timedelta
import csv
import io
import json

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Patient, Doctor, Appointment, Department, MedicalRecord, Prescription, Billing
from .forms import (
    PatientForm, DoctorForm, AppointmentForm, DepartmentForm,
    MedicalRecordForm, PrescriptionForm, BillingForm, UserRegistrationForm
)

def home(request):
    return render(request, 'hospital/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'hospital/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'hospital/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    today = date.today()
    
    # Get statistics
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    today_appointments = Appointment.objects.filter(date=today).count()
    
    # Recent appointments
    recent_appointments = Appointment.objects.filter(
        date__gte=today - timedelta(days=7)
    ).order_by('-date', '-time')[:5]
    
    # Upcoming appointments for today
    upcoming_appointments = Appointment.objects.filter(
        date=today,
        status='scheduled'
    ).order_by('time')[:5]
    
    # Appointment statistics (last 7 days including today)
    start_date = today - timedelta(days=6)
    date_range = [start_date + timedelta(days=i) for i in range(7)]
    counts_by_date = {
        row['date']: row['count']
        for row in Appointment.objects.filter(date__range=(start_date, today))
        .values('date')
        .annotate(count=Count('id'))
    }
    appointment_chart = {
        'labels': [d.strftime('%a') for d in date_range],
        'data': [counts_by_date.get(d, 0) for d in date_range],
    }

    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'recent_appointments': recent_appointments,
        'upcoming_appointments': upcoming_appointments,
        'appointment_chart_json': json.dumps(appointment_chart),
    }
    return render(request, 'hospital/dashboard.html', context)

# Patient views
@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'hospital/patient_list.html', {'patients': patients})

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            try:
                patient = form.save()
                messages.success(request, f'Patient created successfully! ID: {patient.id}')
                return redirect('patient_list')
            except Exception as e:
                messages.error(request, f'Error saving patient: {str(e)}')
        else:
            # Add form errors to messages for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PatientForm()
    return render(request, 'hospital/patient_form.html', {'form': form, 'title': 'Add Patient'})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.all().order_by('-date', '-time')
    medical_records = patient.medical_records.all().order_by('-created_at')
    prescriptions = patient.prescriptions.all().order_by('-created_at')
    bills = patient.bills.all().order_by('-created_at')
    
    context = {
        'patient': patient,
        'appointments': appointments,
        'medical_records': medical_records,
        'prescriptions': prescriptions,
        'bills': bills,
    }
    return render(request, 'hospital/patient_detail.html', context)

@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'hospital/patient_form.html', {'form': form, 'title': 'Edit Patient'})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
        return redirect('patient_list')
    return render(request, 'hospital/patient_confirm_delete.html', {'patient': patient})

# Doctor views
@login_required
def doctor_list(request):
    doctors = Doctor.objects.select_related('department').all()
    return render(request, 'hospital/doctor_list.html', {'doctors': doctors})

@login_required
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor created successfully!')
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'hospital/doctor_form.html', {'form': form, 'title': 'Add Doctor'})

@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = doctor.appointments.all().order_by('-date', '-time')
    medical_records = doctor.medical_records.all().order_by('-created_at')
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'medical_records': medical_records,
    }
    return render(request, 'hospital/doctor_detail.html', context)

@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'hospital/doctor_form.html', {'form': form, 'title': 'Edit Doctor'})

@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor deleted successfully!')
        return redirect('doctor_list')
    return render(request, 'hospital/doctor_confirm_delete.html', {'doctor': doctor})

# Appointment views
@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').all().order_by('-date', '-time')
    doctors = Doctor.objects.all()
    return render(request, 'hospital/appointment_list.html', {'appointments': appointments, 'doctors': doctors})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save()
                messages.success(request, f'Appointment scheduled successfully! ID: {appointment.id}')
                return redirect('appointment_list')
            except Exception as e:
                messages.error(request, f'Error saving appointment: {str(e)}')
        else:
            # Add form errors to messages for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = AppointmentForm()
    
    # Get patients and doctors for the form dropdowns
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'hospital/appointment_form.html', {
        'form': form, 
        'title': 'Schedule Appointment',
        'patients': patients,
        'doctors': doctors
    })

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'hospital/appointment_detail.html', {'appointment': appointment})

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'hospital/appointment_form.html', {'form': form, 'title': 'Edit Appointment'})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('appointment_list')
    return render(request, 'hospital/appointment_confirm_delete.html', {'appointment': appointment})

# Department views
@login_required
def department_list(request):
    departments = Department.objects.select_related('head_of_department').all()
    return render(request, 'hospital/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'hospital/department_form.html', {'form': form, 'title': 'Add Department'})

@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    doctors = department.doctors.all()
    return render(request, 'hospital/department_detail.html', {'department': department, 'doctors': doctors})

@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('department_detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'hospital/department_form.html', {'form': form, 'title': 'Edit Department'})

# Medical Record views
@login_required
def medical_record_create(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = appointment.patient
            medical_record.doctor = appointment.doctor
            medical_record.appointment = appointment
            medical_record.save()
            messages.success(request, 'Medical record created successfully!')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = MedicalRecordForm(initial={
            'patient': appointment.patient,
            'doctor': appointment.doctor,
        })
    return render(request, 'hospital/medical_record_form.html', {
        'form': form, 
        'appointment': appointment,
        'title': 'Create Medical Record'
    })

# Billing views
@login_required
def billing_list(request):
    bills = _get_filtered_bills(request)

    # Calculate totals for summary cards (based on the filtered set)
    total_pending = bills.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
    total_paid = bills.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    total_overdue = bills.filter(status='overdue').aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'hospital/billing_list.html', {
        'bills': bills,
        'total_pending': total_pending,
        'total_paid': total_paid,
        'total_overdue': total_overdue
    })


def _get_filtered_bills(request):
    bills = Billing.objects.select_related('patient').all().order_by('-created_at')

    status = request.GET.get('status')
    if status:
        bills = bills.filter(status=status)

    date_from = request.GET.get('date_from')
    if date_from:
        bills = bills.filter(created_at__date__gte=date_from)

    date_to = request.GET.get('date_to')
    if date_to:
        bills = bills.filter(created_at__date__lte=date_to)

    return bills


@login_required
def billing_export_csv(request):
    bills = _get_filtered_bills(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="billing_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Bill ID', 'Patient', 'Description', 'Amount', 'Status', 'Due Date', 'Paid Date', 'Created At'])

    for bill in bills:
        writer.writerow([
            bill.id,
            bill.patient.full_name,
            bill.description,
            str(bill.amount),
            bill.get_status_display(),
            bill.due_date.isoformat() if bill.due_date else '',
            bill.paid_date.isoformat() if bill.paid_date else '',
            bill.created_at.strftime('%Y-%m-%d %H:%M:%S') if bill.created_at else '',
        ])

    return response


@login_required
def billing_export_pdf(request):
    bills = _get_filtered_bills(request)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    x_left = 40
    y = height - 50

    p.setFont('Helvetica-Bold', 14)
    p.drawString(x_left, y, 'Billing Report')
    y -= 25

    p.setFont('Helvetica', 10)
    p.drawString(x_left, y, f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 20

    # Table header
    p.setFont('Helvetica-Bold', 10)
    p.drawString(x_left, y, 'ID')
    p.drawString(x_left + 40, y, 'Patient')
    p.drawString(x_left + 200, y, 'Amount')
    p.drawString(x_left + 270, y, 'Status')
    p.drawString(x_left + 340, y, 'Due')
    y -= 15
    p.setFont('Helvetica', 9)

    def new_page():
        nonlocal y
        p.showPage()
        y = height - 50
        p.setFont('Helvetica-Bold', 14)
        p.drawString(x_left, y, 'Billing Report (continued)')
        y -= 30
        p.setFont('Helvetica-Bold', 10)
        p.drawString(x_left, y, 'ID')
        p.drawString(x_left + 40, y, 'Patient')
        p.drawString(x_left + 200, y, 'Amount')
        p.drawString(x_left + 270, y, 'Status')
        p.drawString(x_left + 340, y, 'Due')
        y -= 15
        p.setFont('Helvetica', 9)

    for bill in bills:
        if y < 60:
            new_page()

        patient_name = bill.patient.full_name
        if len(patient_name) > 24:
            patient_name = patient_name[:21] + '...'

        status = bill.get_status_display()
        due = bill.due_date.strftime('%Y-%m-%d') if bill.due_date else ''

        p.drawString(x_left, y, f"#{bill.id}")
        p.drawString(x_left + 40, y, patient_name)
        p.drawRightString(x_left + 255, y, f"${bill.amount}")
        p.drawString(x_left + 270, y, status)
        p.drawString(x_left + 340, y, due)
        y -= 14

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="billing_report.pdf"'
    return response

@login_required
def billing_create(request):
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill created successfully!')
            return redirect('billing_list')
    else:
        form = BillingForm()
    return render(request, 'hospital/billing_form.html', {'form': form, 'title': 'Create Bill'})

@login_required
def billing_update(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill updated successfully!')
            return redirect('billing_list')
    else:
        form = BillingForm(instance=bill)
    return render(request, 'hospital/billing_form.html', {'form': form, 'title': 'Edit Bill'})

# API views for AJAX requests
@login_required
def api_patients(request):
    patients = Patient.objects.all()
    data = [{'id': p.id, 'name': f"{p.first_name} {p.last_name}", 'email': p.email} for p in patients]
    return JsonResponse({'patients': data})

@login_required
def api_doctors(request):
    department_id = request.GET.get('department_id')
    if department_id:
        doctors = Doctor.objects.filter(department_id=department_id)
    else:
        doctors = Doctor.objects.all()
    data = [{'id': d.id, 'name': f"Dr. {d.first_name} {d.last_name}", 'specialization': d.specialization} for d in doctors]
    return JsonResponse({'doctors': data})

@login_required
def api_appointments_calendar(request):
    appointments = Appointment.objects.all()
    events = []
    for apt in appointments:
        events.append({
            'title': f"{apt.patient.full_name} - {apt.doctor.full_name}",
            'start': f"{apt.date}T{apt.time}",
            'url': f"/appointments/{apt.id}/"
        })
    return JsonResponse({'events': events})
