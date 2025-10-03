from django.urls import path
from .views import Chat, HealthCheck

urlpatterns = [
    path('health-check/', HealthCheck.as_view(), name='employee_health_check'),
    path('chat/', Chat.as_view(), name='employee_chat'),
]