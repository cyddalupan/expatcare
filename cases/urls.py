from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaseViewSet
from .views import Chat

router = DefaultRouter()
router.register(r'cases', CaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', Chat.as_view(), name='chat'),
]
