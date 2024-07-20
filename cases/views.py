from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from dotenv import load_dotenv
from openai import OpenAI

from .models import Case
from .serializers import CaseSerializer
from employee.models import Employee

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()
