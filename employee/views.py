from django.http import HttpResponse
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
    def get_user(self, passport_number, lastname):
        try:
            # Attempt to find the employee by passport number and last name
            employee = Employee.objects.get(passport_number=passport_number, last_name=lastname)
            # If found, return the employee ID
            return f"\nuser_id:{employee.id}:{employee.first_name} {employee.last_name}"
        except Employee.DoesNotExist:
            # If no such employee exists, return an error message
            return "We can't find you in our list of employees."
    def post(self, request):
        usermessage = request.data.get('message', None)

        messages = [
            {"role": "system", "content": "Your goal is to get the passport number and last name of the user to confirm the identity so you can help. You are comforting to talk to."},
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
            print("completion:")
            print(completion)
            print("Response contrnt:")
            print(response_content)

            tool_calls = completion.choices[0].message.tool_calls
            print("tool_calls:")
            print(tool_calls)

            if tool_calls:
                print("Inside tool_calls")
                function_name = tool_calls[0].function.name 
                print("function name:")
                print(function_name)
                arguments = tool_calls[0].function.arguments 
                arguments_dict = json.loads(arguments)
                print(arguments)

                if function_name == "get_passport":
                    print("function name is get_passport")
                    passport_number = arguments_dict['passport_number']
                    last_name = arguments_dict['last_name']
                    print("passport and lastname:")
                    print(passport_number)
                    print(last_name)
                    user_reponse = self.get_user(passport_number, last_name)
                    print("user_reponse:")
                    print(user_reponse)
                    response_content = user_reponse

            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
