from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActionsGPTWebhook, HelloWorld, TaskViewSet

router = DefaultRouter()
router.register(r'Task', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hello/', HelloWorld.as_view(), name='hello-world'),
    path('actions-gpt-webhook/', ActionsGPTWebhook.as_view(), name='actions-gpt-webhook'),
]
