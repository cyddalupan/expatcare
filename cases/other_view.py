from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from dotenv import load_dotenv
from openai import OpenAI

from .models import Case
from employee.models import Employee

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

class Other(APIView):
    def log_case(self, employee_id, category, summary):
        try:
            # Retrieve the Employee instance
            employee = Employee.objects.get(id=employee_id)

            # Create and save the Case instance
            case = Case.objects.create(
                employee=employee,
                category=category,
                summary=summary
            )

            # Return the specified string message
            return "systeminfo:report:Kakausapin ko ang iyong employer at aayusin ang iyong problema"
        
        except Employee.DoesNotExist:
            # Handle the case where the Employee does not exist
            return "Employee not found"

        except Exception as e:
            # Handle any other exceptions
            return str(e)

    def post(self, request):
        employee_id = request.data.get('employee_id')
        user_message = request.data.get('message')

        # Initial messages for the OpenAI chat
        messages = [
            {"role": "system", "content": "You make sure The user is Ok, If not make sure know the Problem and get as much information as you need. make sure all important information is included. You are comforting to talk to.  make sure the user does not have any more important information to share. Speak in tagalog if user is speaking tagalog. try to keep reply short"},
        ]
        
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "log_case",
                    "description": "Get the problem of user, dont trigger until we sure that we get all the important details about the problem, get the category and the summary.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "problem category, e.g. 'abuse','rape','torture' etc",
                            },
                            "summary": {
                                "type": "string",
                                "description": "The summary of the problem. compile and make it look like a report",
                            },
                        },
                        "required": ["category", "summary"],
                    },
                },
            }
        ]

        if user_message:
            for obj in user_message:
                sender = "user" if obj['sender'] != "AI" else "system"
                messages.append({"role": sender, "content": obj['text']})

        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
            )
            response_content = completion.choices[0].message.content
            tool_calls = completion.choices[0].message.tool_calls
            
            if tool_calls:
                function_name = tool_calls[0].function.name 
                arguments = tool_calls[0].function.arguments 
                arguments_dict = json.loads(arguments)
                
                if function_name == "log_case":
                    category = arguments_dict['category']
                    summary = arguments_dict['summary']
                    user_response = self.log_case(employee_id, category, summary)
                    response_content = user_response

            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
