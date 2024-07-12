from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class HelloWorld(APIView):
    def get(self, request, format=None):
        return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)
    
class ActionsGPTWebhook(APIView):
    def post(self, request, format=None):
        # Assume the incoming JSON has a key "user_input"
        user_input = request.data.get("user_input", "Hello")

        # Process the input or perform actions here
        response_message = f"Echo: {user_input}"

        # Construct the response for ActionsGPT
        return Response({"responses": [{"message": response_message}]}, status=status.HTTP_200_OK)