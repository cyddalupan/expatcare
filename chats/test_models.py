from django.test import TestCase
from django.contrib.auth.models import User
from employee.models import Employee
from chats.models import Chat
import datetime

class ChatModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_chat_creation(self):
        self.assertEqual(self.chat.employee, self.employee)
        self.assertEqual(self.chat.agency, self.user)
        self.assertEqual(self.chat.message, 'Test message')
        self.assertEqual(self.chat.sender, 'Employee')
        self.assertFalse(self.chat.is_support)

    def test_chat_str(self):
        self.assertEqual(str(self.chat), f"Chat by {self.employee} at {self.chat.timestamp}")
