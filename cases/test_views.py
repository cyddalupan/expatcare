import json
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from employee.models import Employee
from support.models import ChatSupport
from unittest.mock import patch
from rest_framework.authtoken.models import Token

class SakloloViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password', email='test@user.com')
        cls.agency = User.objects.create_user(username='agency', password='password')
        cls.employee = Employee.objects.create(
            first_name='Test',
            last_name='User',
            passport_number='12345',
            date_of_birth='2000-01-01',
            address='123 Test St',
            phone_number='1234567890',
            email='test@employee.com',
            agency=cls.agency,
            emergency_contact_name='Test Contact',
            emergency_contact_phone='0987654321',
            country='PH'
        )

    def setUp(self):
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_saklolo_success(self):
        url = reverse('saklolo')
        data = {'employee_id': self.employee.id}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['response'], 'systeminfo$:$support$:$Please Wait...')
        self.assertTrue(ChatSupport.objects.filter(employee=self.employee, is_open=True).exists())
        self.employee.refresh_from_db()
        self.assertTrue(self.employee.is_support)

    def test_saklolo_no_employee_id(self):
        url = reverse('saklolo')
        data = {}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Employee ID required.')

class ChatViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser2', password='password', email='test2@user.com')
        cls.agency = User.objects.create_user(username='agency2', password='password')
        cls.employee = Employee.objects.create(
            first_name='Test',
            last_name='User 2',
            passport_number='54321',
            date_of_birth='2000-01-02',
            address='321 Test St',
            phone_number='0987654321',
            email='test2@employee.com',
            agency=cls.agency,
            emergency_contact_name='Test Contact 2',
            emergency_contact_phone='1234567890',
            country='PH'
        )

    def setUp(self):
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('cases.views.client.chat.completions.create')
    def test_chat_view_success(self, mock_create):
        mock_create.return_value.choices[0].message.content = 'Test response'
        mock_create.return_value.choices[0].message.tool_calls = None
        url = reverse('chat')
        data = {
            'employee_id': self.employee.id,
            'message': [{'sender': 'user', 'text': 'Hello'}],
            'category': 'chat'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['response'], 'Test response')

    def test_chat_view_no_employee_id(self):
        url = reverse('chat')
        data = {
            'message': [{'sender': 'user', 'text': 'Hello'}],
            'category': 'chat'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Employee ID and message are required.')

    def test_chat_view_no_message(self):
        url = reverse('chat')
        data = {
            'employee_id': self.employee.id,
            'category': 'chat'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Employee ID and message are required.')