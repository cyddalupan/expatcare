from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Chat, Saklolo

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', Chat.as_view(), name='chat'),
    path('saklolo/', Saklolo.as_view(), name='saklolo'),
]
