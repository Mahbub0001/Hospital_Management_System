import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from django.contrib.auth.models import User
from hospital_app.models import Patient, Doctor, Department, Appointment, MedicalRecord, Prescription, Billing
from datetime import datetime, date, timedelta
import random

def create_initial_data():
    print("Creating initial data...")
    
    # Create Departments
    departments_data = [
        {'name': 'Cardiology', 'description': 'Heart and cardiovascular system'},
        {'name': 'Neurology', 'description': 'Brain and nervous system'},
        {'name': 'Orthopedics', 'description': 'Bones and joints'},
        {'name': 'Pediatrics', 'description': 'Children healthcare'},
        {'name': 'General Medicine', 'description': 'General healthcare'},
        {'name': 'Emergency', 'description': 'Emergency care'},
    ]
    
    departments = []
    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={'description': dept_data['description']}
        )
        departments.append(dept)
        print(f"Department: {dept.name} - {'Created' if created else 'Already exists'}")
    
    # Create Doctors
    doctors_data = [
        {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@hospital.com',
            'phone': '555-0101',
            'specialization': 'Cardiologist',
            'department': departments[0],
            'license_number': 'MD12345',
            'gender': 'M',
            'qualification': 'MD, FACC',
            'experience_years': 15,
            'consultation_fee': 250.00,
            'available_days': 'Monday, Wednesday, Friday',
            'available_time': '9:00 AM - 5:00 PM'
        },
        {
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'email': 'sarah.johnson@hospital.com',
            'phone': '555-0102',
            'specialization': 'Neurologist',
            'department': departments[1],
            'license_number': 'MD12346',
            'gender': 'F',
            'qualification': 'MD, FAAN',
            'experience_years': 12,
            'consultation_fee': 300.00,
            'available_days': 'Tuesday, Thursday',
            'available_time': '10:00 AM - 6:00 PM'
        },
        {
            'first_name': 'Michael',
            'last_name': 'Brown',
            'email': 'michael.brown@hospital.com',
            'phone': '555-0103',
            'specialization': 'Orthopedic Surgeon',
            'department': departments[2],
            'license_number': 'MD12347',
            'gender': 'M',
            'qualification': 'MD, FAAOS',
            'experience_years': 20,
            'consultation_fee': 350.00,
            'available_days': 'Monday, Tuesday, Thursday, Friday',
            'available_time': '8:00 AM - 4:00 PM'
        },
        {
            'first_name': 'Emily',
            'last_name': 'Davis',
            'email': 'emily.davis@hospital.com',
            'phone': '555-0104',
            'specialization': 'Pediatrician',
            'department': departments[3],
            'license_number': 'MD12348',
            'gender': 'F',
            'qualification': 'MD, FAAP',
            'experience_years': 8,
            'consultation_fee': 200.00,
            'available_days': 'Monday, Wednesday, Friday',
            'available_time': '9:00 AM - 5:00 PM'
        },
        {
            'first_name': 'Robert',
            'last_name': 'Wilson',
            'email': 'robert.wilson@hospital.com',
            'phone': '555-0105',
            'specialization': 'General Practitioner',
            'department': departments[4],
            'license_number': 'MD12349',
            'gender': 'M',
            'qualification': 'MD',
            'experience_years': 10,
            'consultation_fee': 150.00,
            'available_days': 'Monday to Friday',
            'available_time': '8:00 AM - 6:00 PM'
        }
    ]
    
    doctors = []
    for doc_data in doctors_data:
        doctor, created = Doctor.objects.get_or_create(
            email=doc_data['email'],
            defaults=doc_data
        )
        doctors.append(doctor)
        print(f"Doctor: {doctor.full_name} - {'Created' if created else 'Already exists'}")
    
    # Set department heads
    departments[0].head_of_department = doctors[0]
    departments[0].save()
    departments[1].head_of_department = doctors[1]
    departments[1].save()
    departments[2].head_of_department = doctors[2]
    departments[2].save()
    
    # Create Patients
    patients_data = [
        {
            'first_name': 'James',
            'last_name': 'Anderson',
            'email': 'james.anderson@email.com',
            'phone': '555-0201',
            'date_of_birth': date(1985, 5, 15),
            'gender': 'M',
            'blood_type': 'O+',
            'address': '123 Main St, City, State 12345',
            'emergency_contact': 'Mary Anderson',
            'emergency_phone': '555-0202',
            'medical_history': 'Hypertension, controlled with medication',
            'allergies': 'Penicillin'
        },
        {
            'first_name': 'Mary',
            'last_name': 'Thompson',
            'email': 'mary.thompson@email.com',
            'phone': '555-0203',
            'date_of_birth': date(1990, 8, 22),
            'gender': 'F',
            'blood_type': 'A+',
            'address': '456 Oak Ave, City, State 12345',
            'emergency_contact': 'John Thompson',
            'emergency_phone': '555-0204',
            'medical_history': 'Asthma, seasonal allergies',
            'allergies': 'Pollen, dust'
        },
        {
            'first_name': 'David',
            'last_name': 'Martinez',
            'email': 'david.martinez@email.com',
            'phone': '555-0205',
            'date_of_birth': date(1978, 3, 10),
            'gender': 'M',
            'blood_type': 'B+',
            'address': '789 Pine Rd, City, State 12345',
            'emergency_contact': 'Lisa Martinez',
            'emergency_phone': '555-0206',
            'medical_history': 'Type 2 Diabetes',
            'allergies': 'None known'
        },
        {
            'first_name': 'Jennifer',
            'last_name': 'Lee',
            'email': 'jennifer.lee@email.com',
            'phone': '555-0207',
            'date_of_birth': date(1995, 12, 3),
            'gender': 'F',
            'blood_type': 'AB+',
            'address': '321 Elm St, City, State 12345',
            'emergency_contact': 'Kevin Lee',
            'emergency_phone': '555-0208',
            'medical_history': 'Migraines',
            'allergies': 'Shellfish'
        },
        {
            'first_name': 'William',
            'last_name': 'Garcia',
            'email': 'william.garcia@email.com',
            'phone': '555-0209',
            'date_of_birth': date(2005, 7, 18),
            'gender': 'M',
            'blood_type': 'O-',
            'address': '654 Maple Dr, City, State 12345',
            'emergency_contact': 'Susan Garcia',
            'emergency_phone': '555-0210',
            'medical_history': 'No significant medical history',
            'allergies': 'Peanuts'
        }
    ]
    
    patients = []
    for patient_data in patients_data:
        patient, created = Patient.objects.get_or_create(
            email=patient_data['email'],
            defaults=patient_data
        )
        patients.append(patient)
        print(f"Patient: {patient.full_name} - {'Created' if created else 'Already exists'}")
    
    # Create Appointments
    appointments_data = []
    for i in range(20):
        appointment_date = date.today() + timedelta(days=random.randint(-30, 30))
        appointment_time = datetime.strptime(f"{random.randint(9, 16):02d}:00", "%H:%M").time()
        
        appointment_data = {
            'patient': random.choice(patients),
            'doctor': random.choice(doctors),
            'date': appointment_date,
            'time': appointment_time,
            'status': random.choice(['scheduled', 'completed', 'cancelled', 'no_show']),
            'symptoms': random.choice(['Chest pain', 'Headache', 'Joint pain', 'Fever', 'Routine checkup']),
            'notes': f'Appointment note {i+1}'
        }
        appointments_data.append(appointment_data)
    
    appointments = []
    for apt_data in appointments_data:
        appointment, created = Appointment.objects.get_or_create(
            patient=apt_data['patient'],
            doctor=apt_data['doctor'],
            date=apt_data['date'],
            time=apt_data['time'],
            defaults=apt_data
        )
        if created:
            appointments.append(appointment)
        print(f"Appointment: {appointment.patient.full_name} with {appointment.doctor.full_name} - {'Created' if created else 'Already exists'}")
    
    # Create Medical Records for completed appointments
    completed_appointments = Appointment.objects.filter(status='completed')
    for appointment in completed_appointments[:10]:
        medical_record, created = MedicalRecord.objects.get_or_create(
            appointment=appointment,
            defaults={
                'patient': appointment.patient,
                'doctor': appointment.doctor,
                'diagnosis': random.choice(['Hypertension', 'Migraine', 'Arthritis', 'Common cold', 'Healthy']),
                'symptoms': appointment.symptoms,
                'treatment': random.choice(['Medication prescribed', 'Rest recommended', 'Physical therapy', 'Lifestyle changes']),
                'follow_up_date': appointment.date + timedelta(days=7)
            }
        )
        print(f"Medical Record: {medical_record.patient.full_name} - {'Created' if created else 'Already exists'}")
    
    # Create Prescriptions
    medical_records = MedicalRecord.objects.all()[:5]
    prescriptions_data = [
        'Lisinopril 10mg - Once daily',
        'Ibuprofen 400mg - As needed for pain',
        'Metformin 500mg - Twice daily',
        'Albuterol inhaler - As needed',
        'Amoxicillin 500mg - Three times daily'
    ]
    
    for record in medical_records:
        prescription, created = Prescription.objects.get_or_create(
            medical_record=record,
            patient=record.patient,
            doctor=record.doctor,
            defaults={
                'medication': random.choice(prescriptions_data),
                'dosage': '1 tablet',
                'frequency': 'Daily',
                'duration': '30 days',
                'instructions': 'Take with food'
            }
        )
        print(f"Prescription: {prescription.patient.full_name} - {'Created' if created else 'Already exists'}")
    
    # Create Bills
    for appointment in appointments[:15]:
        bill, created = Billing.objects.get_or_create(
            appointment=appointment,
            patient=appointment.patient,
            defaults={
                'description': f'Consultation with {appointment.doctor.full_name}',
                'amount': appointment.doctor.consultation_fee,
                'status': random.choice(['pending', 'paid', 'overdue']),
                'due_date': appointment.date + timedelta(days=30),
                'paid_date': appointment.date + timedelta(days=5) if random.choice([True, False]) else None
            }
        )
        print(f"Bill: {bill.patient.full_name} - ${bill.amount} - {'Created' if created else 'Already exists'}")
    
    print("\nInitial data creation completed!")
    print(f"Departments: {Department.objects.count()}")
    print(f"Doctors: {Doctor.objects.count()}")
    print(f"Patients: {Patient.objects.count()}")
    print(f"Appointments: {Appointment.objects.count()}")
    print(f"Medical Records: {MedicalRecord.objects.count()}")
    print(f"Prescriptions: {Prescription.objects.count()}")
    print(f"Bills: {Billing.objects.count()}")

if __name__ == '__main__':
    create_initial_data()
