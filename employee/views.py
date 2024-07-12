from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

class Chat(APIView):
    def post(self, request):
        usermessage = request.data.get('message', None)

        messages = [
            {"role": "system", "content": "You are a friend that gives good advice. Concern if I have problem. Limit reply to 200 characters."},
        ]

        for obj in usermessage:
            sender = "user" if obj['sender'] != "AI" else "system"
            messages.append({"role": sender, "content": obj['text']})

        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response_content = completion.choices[0].message.content
            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)