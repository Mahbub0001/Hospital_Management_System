import os
import sys
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')

from django.core.wsgi import get_wsgi_application

# Initialize Django application
django_app = get_wsgi_application()

# Vercel Python runtime expects 'app' variable
# This is the WSGI application that handles all requests
app = django_app