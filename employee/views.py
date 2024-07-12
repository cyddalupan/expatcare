from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

class Chat(APIView):
    def get_current_weather(location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        if "tokyo" in location.lower():
            return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
        elif "san francisco" in location.lower():
            return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
        elif "paris" in location.lower():
            return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
        else:
            return json.dumps({"location": location, "temperature": "unknown"})

    def post(self, request):
        usermessage = request.data.get('message', None)

        messages = [
            {"role": "system", "content": "You are a friend that gives good advice. Concern if I have problem. Limit reply to 200 characters."},
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
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

            tool_calls = response_message.tool_calls
            print("All good")

            if tool_calls:
                print("Inside tool_calls")
                function_name = tool_calls['name']
                print("function name:")
                print(function_name)
                arguments = tool_calls['arguments']
                print(arguments)

                if function_name == "get_current_weather":
                    print("function name is get weather")
                    location = arguments.get('location')
                    print("location:")
                    print(location)
                    unit = arguments.get('unit', 'celsius')
                    print(unit)
                    weather_info = get_current_weather(location, unit)
                    print(weather_info)
                    response_content += f"\nWeather Info: {weather_info}"

            return Response({'response': response_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
