from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from dotenv import load_dotenv
from openai import OpenAI
from .models import Case
from employee.models import Employee
from chats.models import Chat
from advance.utils import get_setting

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

class Report(APIView):
    def get_report(self, employee_id, user_want):
        if user_want == "file_new_report":
            return "systeminfo$:$chat$:$Meron ka pang gusto ibahagi, ano pa ang nangyari sayo?"

        if user_want == "just_want_to_talk":
            return "systeminfo$:$chat$:$Kamusta ka naman?"
        
        try:
            # Retrieve the Employee instance
            employee = Employee.objects.get(id=employee_id)

            # Retrieve all cases related to the employee
            cases = Case.objects.filter(employee=employee)

            # Check if any cases are found
            if not cases.exists():
                return "systeminfo$:$chat$:$Wala ka pang nagagawang reklamo, gusto mo ba mag reklamo?."

            # Format the message
            message = f"systeminfo$:$chat$:$Eto ang lagay ng iyong report {employee.first_name} {employee.last_name}:<br/>"
            for case in cases:
                message += f"- {case.category}: {case.get_report_status_display()}<br/>"

            return message

        except Employee.DoesNotExist:
            # Handle the case where the Employee does not exist
            return "Employee not found"

        except Exception as e:
            # Handle any other exceptions
            return str(e)

    def post(self, request):
        employee_id = request.data.get('employee_id', None)
        user_message = request.data.get('message', None)

        if not employee_id or not user_message:
            return Response({'error': 'Employee ID and message are required.'}, status=status.HTTP_400_BAD_REQUEST)

        latest_user_message = user_message[-1]['text'] if user_message else None
        
        if latest_user_message:
            employee = Employee.objects.get(id=employee_id)
            Chat.objects.create(
                employee=employee,
                agency=employee.agency,
                message=latest_user_message,
                is_support=False,
                sender='Employee'
            )

        general_instruction = get_setting('general_instruction', default='')

        messages = [
            {"role": "system", "content": general_instruction + "Ask if they want updates on their previous case/report."},
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_report",
                    "description": "confirm if the user wants to check the report status or wants to create a complaint",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_want": {
                                "type": "string",
                                "enum": ["get_report", "file_new_report", "just_want_to_talk"],
                                "description": "get if user wants to check report status, create a new complaint, or just want to talk",
                            },
                        },
                        "required": ["user_want"],
                    },
                },
            }
        ]

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

                if function_name == "get_report":
                    user_want = arguments_dict['user_want']
                    user_response = self.get_report(employee_id, user_want)
                    response_content = user_response

            if response_content:
                Chat.objects.create(
                    employee=employee,
                    agency=employee.agency,
                    message=response_content,
                    is_support=False,
                    sender='AI'
                )

            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
