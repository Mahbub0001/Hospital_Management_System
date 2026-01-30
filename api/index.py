import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')

application = get_wsgi_application()
