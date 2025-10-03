from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User, Group
from employee.models import Employee
from employee.views import Chat

class ChatViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        agency_group, _ = Group.objects.get_or_create(name="Agency")
        cls.agency_user = User.objects.create_user(
            username="testagency",
            password="testpassword",
            email="testagency@example.com"
        )
        cls.agency_user.groups.add(agency_group)

        cls.employee = Employee.objects.create(
            first_name="Test",
            last_name="User",
            passport_number="P1234567A",
            date_of_birth="1990-01-01",
            address="123 Test St",
            phone_number="1234567890",
            email="test@example.com",
            agency=cls.agency_user,
            country="PH"
        )

    def setUp(self):
        self.client = APIClient()

    @patch('employee.views.client.chat.completions.create')
    def test_chat_get_user_success(self, mock_create):
        """
        Test the chat view's get_user method successfully finds a user.
        """
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = ""
        mock_response.choices[0].message.tool_calls = [
            MagicMock(
                function=MagicMock(
                    name='get_passport',
                    arguments='{"passport_number": "P1234567A", "last_name": "User"}'
                )
            )
        ]
        mock_create.return_value = mock_response

        url = reverse('employee_chat')
        data = {
            "message": [{"sender": "user", "text": "Hello"}],
            "token": "test_token"
        }
        self.client.force_authenticate(user=self.agency_user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(f"user_id:{self.employee.id}:{self.employee.first_name} {self.employee.last_name}", response.data['response'])

    @patch('employee.views.client.chat.completions.create')
    def test_chat_get_user_not_found(self, mock_create):
        """
        Test the chat view's get_user method handles a user not found.
        """
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = ""
        mock_response.choices[0].message.tool_calls = [
            MagicMock(
                function=MagicMock(
                    name='get_passport',
                    arguments='{"passport_number": "P9999999Z", "last_name": "Unknown"}'
                )
            )
        ]
        mock_create.return_value = mock_response

        url = reverse('employee_chat')
        data = {
            "message": [{"sender": "user", "text": "Hello"}],
            "token": "test_token"
        }
        self.client.force_authenticate(user=self.agency_user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['response'], "Hindi kita makita sa listahan namin, Paki double check kung tama ang binigay mong information.")