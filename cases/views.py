import traceback
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from django.http import JsonResponse
from dotenv import load_dotenv
from openai import OpenAI
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
        # topic = request.data.get('category', 'chat') # Temporarily disabled by user request
        # if topic.startswith('$'):
        #     topic = topic[1:]
        topic = 'chat' # Temporarily forced by user request
        print(f'TOPIC: {topic}')

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

        try:
            if topic != 'chat':
                category = get_object_or_404(AICategory, category_name=topic)
                categoryRole = category.role
        except Exception as e:
            return Response({'error': f'Error getting category: {str(e)}'}, status=status.HTTP_404_NOT_FOUND)

        general_instruction = '''You are the AI Complaints Assistant for a recruitment agency specializing in placing Overseas Filipino Workers (OFWs).
Core Objective: Your primary function is to professionally receive, document, and process complaints or serious concerns from applicants, ensuring their issues are promptly handed over to the correct internal department for resolution. You must maintain focus entirely on the agency's internal processes and support the applicant from the initial report until the resolution process is complete.
Assistant Protocol:
 * Welcome and Introduction: Begin the chat with a warm welcome. Clearly state your purpose: to officially receive and record their complaint/concern and ensure it is escalated immediately to the appropriate team within the agency for action.
 * Empathy and Active Listening: Listen attentively and show genuine empathy and concern for the applicant's situation. Maintain a calm, polite, and understanding demeanor at all times.
 * Detailed Information Gathering: Systematically collect all crucial details related to the complaint. Use clear questions to gather:
   * What happened (The nature of the complaint)?
   * When did it happen (Date and approximate time)?
   * Where did it occur (Location or context)?
   * How many times has this happened (Frequency)?
   * Applicant Name and Contact Information (phone/email).
 * Escalation and Assurance: Reiterate that you have accurately recorded the details and will immediately transmit the complaint to the designated internal department or officer for handling. Explain that this team will take the necessary steps to resolve the issue.
 * Closing Message: End the interaction with an assuring and respectful closing message, confirming that the agency is now managing their concern and will provide updates as they become available.
DOS and DON'TS for the AI Assistant
DOs
 * Be Respectful and Calm: Be polite, patient, and professional in every response.
 * Show Malasakit (Empathy): Acknowledge the applicant's feelings and validate their concern.
 * Organize Information: Structure the collected complaint details clearly for easy handover.
 * Maintain Focus: Keep the conversation centered on the applicant's issue and the agency's internal resolution process.
 * Provide Assurance: Give an assuring closing message confirming the agency is now handling the issue.
DON'TS
 * Do Not Promise Solutions: Never guarantee a specific outcome or timeline for resolution.
 * Do Not Suggest Government Agencies: Absolutely do not mention, recommend, or refer the applicant to any external government bodies (like OWWA, POEA, DMW, etc.).
 * Do Not Engage in Debate: Avoid arguing or questioning the validity of the complaint. Your role is to receive and process.
 * Do Not Provide Legal Advice: Stick strictly to the agency's intake protocol.'''

        messages = [
            {"role": "system", "content": (general_instruction or "") + (categoryRole or "") + "Talk in taglish. Use common words only. Keep reply short"},
            {"role": "system", "content": f"Employee Name: {employee_name}"},
        ]
        messages.extend(memory_messages)
        messages.extend(case_messages) 
        # tools = [
        #     get_support_json_function,
        #     save_memory_json_function,
        #     get_report_json_function,
        # ] # Temporarily disabled by user request

        # if category:
        #     tools.append(log_case_json_function(category))
        #     tools.append(abort_json_function(topic))
        # else:
        #     tools.append(get_category_json_function(category_names_list)),

        for obj in user_message:
            sender = "user" if obj['sender'] != "AI" else "system"
            messages.append({"role": sender, "content": obj['text']})

        try:
            print("PROMPT_MESSAGES:", messages)
            completion = client.chat.completions.create(
                model="o4-mini",
                messages=messages,
                # tools=tools, # Temporarily disabled by user request
            )
            response_content = completion.choices[0].message.content
            print("#####", completion)
            
            # tool_calls = completion.choices[0].message.tool_calls # Temporarily disabled by user request
            # if tool_calls:
            #     function_name = tool_calls[0].function.name 
            #     arguments = tool_calls[0].function.arguments 
            #     arguments_dict = json.loads(arguments)
                
            #     if function_name == "get_support":
            #         ChatSupport.objects.create(
            #             employee=employee,
            #             last_message=latest_user_message,
            #             is_open=True
            #         )
            #         employee.is_support = True
            #         employee.save()
            #         response_content = "systeminfo$:$support$:$Please Wait..."

            #     if function_name == "abort":
            #         response_content = "systeminfo$:$chat$:$"+response_content
                
            #     if function_name == "log_case" and category:
            #         user_response = log_case(employee_id, category, arguments)
            #         if user_response:
            #             response_content = user_response

            #     if function_name == "get_report":
            #         user_response = get_report(employee_id)
            #         response_content = user_response
                
            #     if function_name == "get_category":
            #         try:
            #             category = arguments_dict['category']
            #             welcome_message = get_object_or_404(AICategory, category_name=category).welcome_message
            #             user_response = get_category(category, welcome_message)
            #             response_content = user_response
            #         except Exception as e:
            #             response_content = f'Error getting category: {str(e)}'

            #     if function_name == "save_memory":
            #         memory_content = arguments_dict['memory_content']
            #         save_memory(employee_id, memory_content)
            #         response_content = "Tatandaan ko to " + employee_name

            if response_content:
                ChatModel.objects.create(
                    employee=employee,
                    agency=employee.agency,
                    message=response_content,
                    sender='AI',
                    is_support=False
                )

            return Response({'reply': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()


class TestView(APIView):
    def get(self, request):
        return Response({'message': 'This is a test view.'}, status=status.HTTP_200_OK)

class Saklolo(APIView):
    def post(self, request):
        employee_id = request.data.get('employee_id', None)
        initial_reply = "systeminfo$:$support$:$Please Wait..."

        if not employee_id:
            return Response({'error': 'Employee ID required.'}, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.get(id=employee_id)
        ChatSupport.objects.create(
            employee=employee,
            last_message="SAKLOLO",
            is_open=True
        )
        ChatModel.objects.create(
            employee=employee,
            agency=employee.agency,
            message=initial_reply,
            sender='AI',
            is_support=True
        )

        employee.is_support = True
        employee.save()
        return Response({'reply': initial_reply}, status=status.HTTP_200_OK)