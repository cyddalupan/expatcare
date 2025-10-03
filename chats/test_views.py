from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from employee.models import Employee
from chats.models import Chat
from support.models import ChatSupport
import datetime
import json

class ChatViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            passport_number='AB123456',
            date_of_birth=datetime.date(1990, 1, 1),
            address='123 Main St',
            phone_number='123-456-7890',
            email='john.doe@example.com',
            country='PH',
            agency=cls.user,
            emergency_contact_name="Jane Doe",
            emergency_contact_phone="987-654-3210",
            token='test-token'
        )
        for i in range(15):
            Chat.objects.create(
                employee=cls.employee,
                agency=cls.user,
                message=f'Test message {i}',
                sender='Employee'
            )

    def test_chat_history_view(self):
        url = reverse('chat-history')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.employee.token}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['chat_history']), 12)
        self.assertEqual(data['chat_history'][0]['message'], 'Test message 3')

    def test_chat_history_view_unauthorized(self):
        url = reverse('chat-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_check_last_reply_closed(self):
        ChatSupport.objects.create(employee=self.employee, is_open=False)
        url = reverse('check-last-reply')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.employee.token}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['response'], 'closed')

    def test_check_last_reply_reply(self):
        Chat.objects.create(employee=self.employee, agency=self.user, message='Support message', sender='AI', is_support=True)
        url = reverse('check-last-reply')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.employee.token}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['response'], 'reply')

    def test_check_last_reply_none(self):
        url = reverse('check-last-reply')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.employee.token}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['response'], 'none')