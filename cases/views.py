import traceback
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from django.http import JsonResponse
from dotenv import load_dotenv
from openai import OpenAI
from advance.utils import get_setting
from .json_functions import abort_json_function, get_category_json_function, log_case_json_function, save_memory_json_function, get_report_json_function, get_support_json_function
from .functions import get_category, log_case, save_memory, get_report
from .models import Case
from support.models import ChatSupport
from chats.models import Chat as ChatModel
from employee.models import Employee, EmployeeMemory
from advance.models import AICategory


load_dotenv()

client = OpenAI()

class Chat(APIView):
    def post(self, request):
        employee_id = request.data.get('employee_id', None)
        user_message = request.data.get('message', None)
        topic = request.data.get('category', 'chat')

        category = None
        categoryRole = None
        
        if not employee_id or not user_message:
            return Response({'error': 'Employee ID and message are required.'}, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.get(id=employee_id)
        employee_name = f"{employee.first_name} {employee.last_name}" 

        category_names = AICategory.objects.values_list('category_name', flat=True)
        category_names_list = list(category_names)
        latest_user_message = user_message[-1]['text'] if user_message else None

        previous_cases = Case.objects.filter(employee=employee).order_by('-date_reported')
        case_messages = [{"role": "system", "content": f"Case and past experience: {case.category} - Status: {case.report_status}"} for case in previous_cases]

        memories = EmployeeMemory.objects.filter(employee=employee).order_by('-created_at')
        memory_messages = [{"role": "system", "content": f"Memory: {memory.note}"} for memory in memories]

        # Save Last Message
        if latest_user_message:
            ChatModel.objects.create(
                employee=employee,
                agency=employee.agency,
                message=latest_user_message,
                sender='Employee',
                is_support=False
            )

        if topic == 'support':
            return Response({'response': "systeminfo$:$support$:$Please wait..."}, status=status.HTTP_200_OK)

        if topic != 'chat':
            category = get_object_or_404(AICategory, category_name=topic)
            categoryRole = category.role

        general_instruction = get_setting('general_instruction', default='')

        messages = [
            {"role": "system", "content": (general_instruction or "") + (categoryRole or "") + "Talk in taglish. Use common words only. Keep reply short"},
            {"role": "system", "content": f"Employee Name: {employee_name}"},
        ]
        messages.extend(memory_messages)
        messages.extend(case_messages) 
        tools = [
            get_support_json_function,
            save_memory_json_function,
            get_report_json_function,
        ]

        if category:
            tools.append(log_case_json_function(category))
            tools.append(abort_json_function(topic))
        else:
            tools.append(get_category_json_function(category_names_list)),

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
            print("#####", completion)
            
            tool_calls = completion.choices[0].message.tool_calls
            if tool_calls:
                function_name = tool_calls[0].function.name 
                arguments = tool_calls[0].function.arguments 
                arguments_dict = json.loads(arguments)
                
                if function_name == "get_support":
                    ChatSupport.objects.create(
                        employee=employee,
                        last_message=latest_user_message,
                        is_open=True
                    )
                    employee.is_support = True
                    employee.save()
                    response_content = "systeminfo$:$support$:$Please Wait"

                if function_name == "abort":
                    response_content = "systeminfo$:$chat$:$"+response_content
                
                if function_name == "log_case" and category:
                    user_response = log_case(employee_id, category, arguments)
                    if user_response:
                        response_content = user_response

                if function_name == "get_report":
                    user_response = get_report(employee_id)
                    response_content = user_response
                
                if function_name == "get_category":
                    category = arguments_dict['category']
                    welcome_message = get_object_or_404(AICategory, category_name=category).welcome_message
                    user_response = get_category(category, welcome_message)
                    response_content = user_response

                if function_name == "save_memory":
                    memory_content = arguments_dict['memory_content']
                    save_memory(employee_id, memory_content)
                    response_content = "Tatandaan ko to " + employee_name

            if response_content:
                ChatModel.objects.create(
                    employee=employee,
                    agency=employee.agency,
                    message=response_content,
                    sender='AI',
                    is_support=False
                )

            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
