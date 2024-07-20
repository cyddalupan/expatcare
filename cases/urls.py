from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cases.chat_view import Chat
from cases.other_view import Other
from cases.report_view import Report

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('other/', Other.as_view(), name='other'),
    path('chat/', Chat.as_view(), name='chat'),
    path('report/', Report.as_view(), name='report'),
]
