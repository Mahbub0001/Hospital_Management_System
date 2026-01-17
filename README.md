# Hospital Management System

A comprehensive full-stack hospital management system built with Django (backend) and HTML/CSS/JavaScript (frontend).

## Features

### Core Functionality
- **Patient Management**: Complete patient records, medical history, and contact information
- **Doctor Management**: Doctor profiles, specializations, schedules, and availability
- **Appointment System**: Schedule, manage, and track patient appointments
- **Department Management**: Organize hospital departments and assign heads
- **Medical Records**: Maintain comprehensive medical records and diagnoses
- **Prescription Management**: Create and manage patient prescriptions
- **Billing System**: Generate and track bills, payments, and invoices

### Advanced Features
- **Interactive Dashboard**: Real-time statistics and overview
- **Search & Filtering**: Advanced search and filtering capabilities
- **Responsive Design**: Mobile-friendly interface
- **Data Visualization**: Charts and graphs for insights
- **User Authentication**: Secure login and registration system
- **API Endpoints**: RESTful API for integration

## Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **SQLite**: Database (development)
- **Python 3.12+**: Programming language

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling with Bootstrap 5
- **JavaScript**: Interactivity and dynamic features
- **Chart.js**: Data visualization
- **Font Awesome**: Icons

## Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd hospital-management
   ```

2. **Create and activate virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create initial data**
   ```bash
   python initial_data.py
   ```

6. **Create superuser (if not already created)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Default Login Credentials

- **Username**: admin
- **Password**: admin123

## Project Structure

```
hospital-management/
├── hospital/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── hospital_app/            # Main application
│   ├── __init__.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL routing
│   ├── forms.py             # Form classes
│   ├── api_views.py         # API viewsets
│   ├── api_urls.py          # API URL routing
│   └── serializers.py       # API serializers
├── hospital/templates/      # HTML templates
│   └── hospital/            # Template files
├── hospital/static/         # Static files
│   ├── css/                 # CSS files
│   ├── js/                  # JavaScript files
│   └── images/              # Image files
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── initial_data.py          # Sample data creation
└── README.md               # This file
```

## Models Overview

### Core Models
- **Patient**: Patient information, medical history, contact details
- **Doctor**: Doctor profiles, specializations, availability
- **Appointment**: Appointment scheduling and management
- **Department**: Hospital departments and organization
- **MedicalRecord**: Patient medical records and diagnoses
- **Prescription**: Medication prescriptions
- **Billing**: Invoice and payment management

## Key Features in Detail

### Dashboard
- Real-time statistics (patients, doctors, appointments)
- Today's appointments overview
- Recent activity feed
- Interactive charts and visualizations

### Patient Management
- Complete patient profiles with medical history
- Search and filter patients
- Track appointments and medical records
- Emergency contact information

### Doctor Management
- Doctor profiles with specializations
- Schedule and availability management
- Department assignments
- Appointment history

### Appointment System
- Schedule appointments with ease
- Calendar view and list view
- Status tracking (scheduled, completed, cancelled)
- Automated time slot management

### Billing System
- Generate bills for consultations
- Track payment status
- Export reports (CSV, PDF)
- Payment history

## API Endpoints

The system includes RESTful API endpoints for:
- `/api/patients/` - Patient management
- `/api/doctors/` - Doctor management
- `/api/appointments/` - Appointment management
- `/api/departments/` - Department management

## Security Features
- User authentication and authorization
- CSRF protection
- Input validation and sanitization
- Secure password handling

## Responsive Design
- Mobile-first approach
- Bootstrap 5 framework
- Touch-friendly interface
- Optimized for all screen sizes

## Development Notes

### Adding New Features
1. Create models in `hospital_app/models.py`
2. Add forms in `hospital_app/forms.py`
3. Create views in `hospital_app/views.py`
4. Add URL patterns in `hospital_app/urls.py`
5. Create templates in `hospital/templates/hospital/`

### Database Changes
```bash
python manage.py makemigrations
python manage.py migrate
```

### Running Tests
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Feel free to use and modify as needed.

## Support

For questions or issues, please refer to the Django documentation or create an issue in the project repository.

---

**Note**: This is a demonstration project. For production use, additional security measures, testing, and optimization would be required.
