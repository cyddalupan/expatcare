from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Chat
from employee.models import Employee
from django.shortcuts import get_object_or_404

class ChatHistoryView(APIView):
    def get(self, request, employee_id):
        # Fetch the employee based on the provided ID
        employee = get_object_or_404(Employee, id=employee_id)
        
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
