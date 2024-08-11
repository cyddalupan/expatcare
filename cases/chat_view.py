from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from dotenv import load_dotenv
from openai import OpenAI
from advance.utils import get_setting

from advance.models import AICategory

load_dotenv()

client = OpenAI()

class Chat(APIView):
    def get_category(self, category, welcome_message):
        return "systeminfo$:$" + (category or "") + "$:$" + (welcome_message or "")
    
    def want_report(self):
        return "systeminfo$:$report$:$Tama ba na gusto mo tignan ang status ng nakaraan mong reklamo?"

    def post(self, request):
        employee_id = request.data.get('employee_id', None)
        usermessage = request.data.get('message', None)
        
        category_names = AICategory.objects.values_list('category_name', flat=True)
        category_names_list = list(category_names)

        general_instruction = get_setting('general_instruction', default='')

        messages = [
            {"role": "system", "content": (general_instruction or "") + "Ensure the user is okay; if not, identify the problem category."},
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_category",
                    "description": "Get the Category of the problem",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": category_names_list,
                                "description": "problem category",
                            },
                        },
                        "required": ["category"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "want_report",
                    "description": "check if user want to see the previous case/reports status",
                },
            }
        ]

        for obj in usermessage:
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
                
                if function_name == "get_category":
                    category = arguments_dict['category']
                    welcome_message = get_object_or_404(AICategory, category_name=category).welcome_message
                    user_response = self.get_category(category, welcome_message)
                    response_content = user_response
                
                if function_name == "want_report":
                    user_response = self.want_report()
                    response_content = user_response

            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
