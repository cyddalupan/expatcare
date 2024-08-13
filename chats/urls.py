from django.urls import path
from .views import ChatHistoryView

urlpatterns = [
    path('chat-history/<int:employee_id>/', ChatHistoryView.as_view(), name='chat-history'),
]
