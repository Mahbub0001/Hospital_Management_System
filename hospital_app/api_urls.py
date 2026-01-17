from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PatientViewSet, DoctorViewSet, AppointmentViewSet, DepartmentViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
