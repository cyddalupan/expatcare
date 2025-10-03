from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from employee.models import Employee
from chats.models import Chat
import datetime

class ChatAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.admin_user = User.objects.create_superuser(username='admin', password='password')
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
        )
        cls.chat = Chat.objects.create(
            employee=cls.employee,
            agency=cls.user,
            message='Test message',
            sender='Employee'
        )

    def test_chat_admin_list_view(self):
        self.client.login(username='admin', password='password')
        url = reverse('admin:chats_chat_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)