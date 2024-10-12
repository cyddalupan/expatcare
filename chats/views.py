from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from support.models import ChatSupport
from .models import Chat
from employee.models import Employee
from django.shortcuts import get_object_or_404

class ChatHistoryView(APIView):
    def get(self, request, employee_id, token):
        # Fetch the employee based on the provided ID
        employee = get_object_or_404(Employee, id=employee_id)
        if token != "null":
            # Save token
            employee.token = token
            employee.save()
        
        # Fetch the last 12 chat messages for this employee
        chat_history = Chat.objects.filter(employee=employee).order_by('-timestamp')[:12]
        
        chat_history = reversed(chat_history)

        # Serialize the chat history (assuming you have a serializer or simply use dicts)
        chat_data = [
            {
                'message': chat.message,
                'sender': chat.sender,
                'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            } for chat in chat_history
        ]

        # Return the chat data in the response
        return Response({'chat_history': chat_data}, status=status.HTTP_200_OK)

class CheckLastReplyView(APIView):
    def get(self, request, employee_id):
        # Fetch the employee based on the provided ID
        employee = get_object_or_404(Employee, id=employee_id)

        # Get the latest chat support instance for this employee
        last_chat_support = ChatSupport.objects.filter(employee=employee).order_by('-created_date').first()

        # Check if there is a support chat and if it's closed
        if last_chat_support and not last_chat_support.is_open:
            return Response({'response': 'closed'}, status=status.HTTP_200_OK)

        # Get the latest chat message for this employee
        last_chat = Chat.objects.filter(employee=employee).order_by('-timestamp').first()

        # Check if there is a message and if the last sender is support
        if last_chat and last_chat.is_support:
            return Response({'response': 'reply'}, status=status.HTTP_200_OK)

        # Otherwise, return false
        return Response({'response': 'none'}, status=status.HTTP_200_OK)
