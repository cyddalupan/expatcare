from django.urls import path
from .views import ChatHistoryView, CheckLastReplyView

urlpatterns = [
    path('chat-history/<int:employee_id>/<str:token>/', ChatHistoryView.as_view(), name='chat-history'),
    path('check-last-reply/<int:employee_id>/', CheckLastReplyView.as_view(), name='check-last-reply'),
]
