from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

class Chat(APIView):
    def get_category(self, category):
        if category == "rape":
            return "systeminfo:" + category + ":Tutulungan ka namin, maari mo ba sabihin kung kailan ito nangyari?"
        else:
            return "systeminfo:" + category + ":Maari mo pa ba ko bigyan ng mga detalye"

    def post(self, request):
        employee_id = request.data.get('employee_id', None)
        usermessage = request.data.get('message', None)

        messages = [
            {"role": "system", "content": "Your are comforting to talk to. make sure the user is ok, if not find out what is the category of the problem. use tagalog if posible"},
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
                                "enum": ["abuse", "rape", "torture", "other"],
                                "description": "problem category",
                            },
                        },
                        "required": ["category"],
                    },
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
                    user_response = self.get_category(category)
                    response_content = user_response

            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
