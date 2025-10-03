import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create a handler
handler = logging.FileHandler('/var/www/api.welfareph.com/employee_chat.log', encoding='utf-8')
# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)

from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
import json
from dotenv import load_dotenv
from openai import OpenAI

from employee.models import Employee
from django.contrib.auth.models import User

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(timeout=120.0)

class HealthCheck(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return HttpResponse("Hello, world!")

    def post(self, request):
        logger.info(f"HealthCheck received a {request.method} request.")
        return HttpResponse("POST request received!")

class Chat(APIView):
    permission_classes = [AllowAny]
    
    def get_user(self, passport_number, lastname, token):
        try:
            # Attempt to find the employee by passport number and last name (case-insensitive)
            employee = Employee.objects.get(
                passport_number__iexact=passport_number.lower(),
                last_name__iexact=lastname.lower()
            )

            # Ensure a User instance is linked to the Employee for token generation
            if not employee.user:
                # Create a new User instance if one doesn't exist
                # Using passport_number as username for uniqueness, password can be random as it's not used for direct login
                username = employee.passport_number
                # Ensure username is unique, append a suffix if necessary
                suffix = 0
                while User.objects.filter(username=username).exists():
                    suffix += 1
                    username = f"{employee.passport_number}_{suffix}"

                new_user = User.objects.create_user(username=username, password=User.objects.make_random_password())
                employee.user = new_user
                employee.save()

            # Get or create a token for the employee's linked User
            token_obj, created = Token.objects.get_or_create(user=employee.user)
            employee.token = token_obj.key
            employee.save()
            # If found, return the employee ID and the generated token
            return f"user_id:{employee.id}:_:{token_obj.key}:{employee.first_name} {employee.last_name}"
        except Employee.DoesNotExist:
            # If no such employee exists, return an error message
            return "Hindi kita makita sa listahan namin, Paki double check kung tama ang binigay mong information."

    def get(self, request):
        logger.info("Chat view received a GET request.")
        return HttpResponse("GET request received!")

    def post(self, request):
        logger.info(f"Incoming request data: {request.data}")
        try:
            usermessage = request.data.get('message', None)
            token = request.data.get('token', "")

            employee = None
            if token:
                try:
                    employee = Employee.objects.get(token=token)
                    logger.info(f"Authenticated employee: {employee.first_name} {employee.last_name}")
                except Employee.DoesNotExist:
                    logger.warning(f"Token {token} provided but no matching employee found.")
            
            if employee:
                system_prompt = "You are a helpful assistant for overseas Filipino workers. Talk in taglish. Use common words only. Keep reply short."
                tools = [] # No tools for authenticated chat, or define specific tools if needed later
            else:
                system_prompt = "Your goal is to get the passport number and last name of the user to confirm the identity so you can help. You are comforting to talk to. Talk in taglish. Use common words only. Keep reply short"
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
            
            messages = [
                {"role": "system", "content": system_prompt},
            ]

            for obj in usermessage:
                sender = "user" if obj['sender'] != "AI" else "assistant"
                messages.append({"role": sender, "content": obj['text']})
            
            logger.info(f"Messages sent to OpenAI: {messages}")

            print("PROMPT_EMPLOYEE_VIEWS_CHAT:", messages)
            # First API call to check for tool use
            response = client.chat.completions.create(
                model="o4-mini",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                logger.info(f"OpenAI requested tool call: {tool_calls}")
                messages.append(response_message)
                
                tool_call = tool_calls[0]
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                function_response = self.get_user(
                    passport_number=function_args.get("passport_number"),
                    lastname=function_args.get("last_name"),
                    token=token
                )
                
                logger.info(f"Tool function '{function_name}' returned: {function_response}")

                if function_response.startswith("user_id:"):
                    parts = function_response.split(':')
                    user_id = parts[1]
                    extracted_token = parts[3]
                    full_name = parts[4] # Corrected to use parts[4] directly

                    # Get AI's welcome message
                    welcome_messages = [
                        {"role": "system", "content": "You are a helpful assistant for overseas Filipino workers. Respond with a short, comforting welcome message in Taglish."},
                        {"role": "user", "content": f"The user {full_name} (ID: {user_id}) has just been authenticated. Welcome them."}
                    ]
                    welcome_completion = client.chat.completions.create(
                        model="o4-mini",
                        messages=welcome_messages,
                        stream=False,
                    )
                    ai_welcome_message = welcome_completion.choices[0].message.content

                    return Response({
                        "status": "authenticated",
                        "userId": user_id,
                        "token": extracted_token,
                        "fullName": full_name,
                        "message": ai_welcome_message
                    }, status=status.HTTP_200_OK)
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

                # Second API call to get the final user-facing response
                def stream_response():
                    try:
                        print("PROMPT_EMPLOYEE_VIEWS_CHAT_TOOL_CALL:", messages)
                        completion = client.chat.completions.create(
                            model="o4-mini",
                            messages=messages,
                            stream=True,
                        )
                        for chunk in completion:
                            content = chunk.choices[0].delta.content
                            if content:
                                yield content
                    except Exception as e:
                        logger.error(f"An error occurred during streaming response: {e}", exc_info=True)
                        yield "Pasensya na, nagkaroon ng technical issue sa streaming. Pakisubukang muli."
                
                return StreamingHttpResponse(stream_response(), content_type="text/event-stream")
            
            else:
                # If no tool is called, return the response directly as JSON
                ai_message_content = response.choices[0].message.content
                return Response({"status": "success", "message": ai_message_content}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"An error occurred in Chat view: {e}", exc_info=True)
            # Return a generic error message in the stream
            def error_stream():
                yield "Pasensya na, nagkaroon ng technical issue. Pakisubukang muli."
            return StreamingHttpResponse(error_stream(), content_type="text/event-stream", status=500)
