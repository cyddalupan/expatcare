from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from dotenv import load_dotenv
from openai import OpenAI

from advance.models import AICategory
from advance.utils import get_setting

from .models import Case
from employee.models import Employee

load_dotenv()

client = OpenAI()

class Wellbeing(APIView):
    def log_case(self, employee_id, category, arguments):
        arguments_dict = json.loads(arguments)
        readable_format = "\n".join([f"{key.capitalize()}: {value}" for key, value in arguments_dict.items()])

        try:
            employee = Employee.objects.get(id=employee_id)
            
            # Check if a case exists for the employee with the same category
            try:
                case = Case.objects.get(employee=employee, category=category)
                # Update the existing report
                case.report = readable_format
                case.save()
            except Case.DoesNotExist:
                # Create a new case
                case = Case.objects.create(
                    employee=employee,
                    category=category,
                    report=readable_format,
                    agency=employee.agency
                )

            # Check if all required parameters are present
            all_expected_params = self.get_param_names(category)
            provided_params = arguments_dict.keys()

            if set(all_expected_params) <= set(provided_params):
                # All required parameters are present
                return "systeminfo$:$report$:$" + category.closing_message
            else:
                # Not all required parameters are present
                return None

        except Employee.DoesNotExist:
            return "Employee not found"
        except Exception as e:
            return str(e)
        
    def get_properties(self, category):
        properties = {}
        if category.param_one_name and category.param_one_name.strip():
            properties[category.param_one_name] = {
                "type": "string",
                "description": category.param_one_desc,
            }
            if category.param_one_enum and category.param_one_enum.strip():
                properties[category.param_one_name]["enum"] = category.param_one_enum.split(',')
        
        if category.param_two_name and category.param_two_name.strip():
            properties[category.param_two_name] = {
                "type": "string",
                "description": category.param_two_desc,
            }
            if category.param_two_enum and category.param_two_enum.strip():
                properties[category.param_two_name]["enum"] = category.param_two_enum.split(',')
        
        if category.param_three_name and category.param_three_name.strip():
            properties[category.param_three_name] = {
                "type": "string",
                "description": category.param_three_desc,
            }
            if category.param_three_enum and category.param_three_enum.strip():
                properties[category.param_three_name]["enum"] = category.param_three_enum.split(',')
        
        if category.param_four_name and category.param_four_name.strip():
            properties[category.param_four_name] = {
                "type": "string",
                "description": category.param_four_desc,
            }
            if category.param_four_enum and category.param_four_enum.strip():
                properties[category.param_four_name]["enum"] = category.param_four_enum.split(',')
        
        properties["summary"] = {
            "type": "string",
            "description": "The summary of the problem. Compile and make it look like a report.",
        }
        return properties

    def get_param_names(self, category):
        param_names = []
        if category.param_one_name and category.param_one_name.strip():
            param_names.append(category.param_one_name)
        if category.param_two_name and category.param_two_name.strip():
            param_names.append(category.param_two_name)
        if category.param_three_name and category.param_three_name.strip():
            param_names.append(category.param_three_name)
        if category.param_four_name and category.param_four_name.strip():
            param_names.append(category.param_four_name)
        param_names.append("summary")
        return param_names

    def post(self, request):
        employee_id = request.data.get('employee_id')
        topic = request.data.get('category')
        user_message = request.data.get('message')

        category = get_object_or_404(AICategory, category_name=topic)
        general_instruction = get_setting('general_instruction', default='')

        messages = [
            {"role": "system", "content": general_instruction + category.role},
        ]
        
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "log_case",
                    "description": category.function_description,
                    "parameters": {
                        "type": "object",
                        "properties": self.get_properties(category),
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "abort",
                    "description": "The topic is "+topic+". Check if the user wants to abort the report or automatically abort if unrelated topics are discussed.",
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
                
                if function_name == "log_case":
                    user_response = self.log_case(employee_id, category, arguments)
                    if user_response:
                        response_content = user_response
                    # If user_response is None, keep response_content as the original OpenAI response

                if function_name == "abort":
                    response_content = "systeminfo$:$chat$:$Kung sakaling mayroon kang problema sabihin mo lang agad saakin"

            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
