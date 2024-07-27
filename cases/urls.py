from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cases.chat_view import Chat
from cases.wellbeing_view import Wellbeing
from cases.report_view import Report

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('wellbeing/', Wellbeing.as_view(), name='wellbeing'),
    path('chat/', Chat.as_view(), name='chat'),
    path('report/', Report.as_view(), name='report'),
]
