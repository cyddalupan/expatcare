from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from dotenv import load_dotenv
from openai import OpenAI

from employee.models import Employee

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

class Chat(APIView):
    def get_user(self, passport_number, lastname, token):
        try:
            # Attempt to find the employee by passport number and last name (case-insensitive)
            employee = Employee.objects.get(
                passport_number__iexact=passport_number.lower(),
                last_name__iexact=lastname.lower()
            )
            employee.token = token
            employee.save()
            # If found, return the employee ID
            return f"user_id:{employee.id}:{employee.first_name} {employee.last_name}"
        except Employee.DoesNotExist:
            # If no such employee exists, return an error message
            return "Hindi kita makita sa listahan namin, Paki double check kung tama ang binigay mong information."

    def post(self, request):
        usermessage = request.data.get('message', None)
        token = request.data.get('token', "")

        messages = [
            {"role": "system", "content": "Your goal is to get the passport number and last name of the user to confirm the identity so you can help. You are comforting to talk to. Talk in taglish. Use common words only. Keep reply short"},
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_passport",
                    "description": "Get the passport number and last name of the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "passport_number": {
                                "type": "string",
                                "description": "passport number, e.g. 'P1234567A' or 'EC1234567.'",
                            },
                            "last_name": {
                                "type": "string",
                                "description": "the last name,e.g. 'Santos' or 'Dela Cruz.'",
                            },
                        },
                        "required": ["passport_number", "last_name"],
                    },
                },
            }
        ]

        for obj in usermessage:
            sender = "user" if obj['sender'] != "AI" else "system"
            messages.append({"role": sender, "content": obj['text']})

        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=tools,
            )
            response_content = completion.choices[0].message.content
            tool_calls = completion.choices[0].message.tool_calls
            
            if tool_calls:
                function_name = tool_calls[0].function.name 
                arguments = tool_calls[0].function.arguments 
                arguments_dict = json.loads(arguments)
                
                if function_name == "get_passport":
                    passport_number = arguments_dict['passport_number']
                    last_name = arguments_dict['last_name']
                    user_reponse = self.get_user(passport_number, last_name, token)
                    response_content = user_reponse

            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
