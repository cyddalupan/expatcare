
from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Employee, EmployeeMemory

class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        agency_group, created = Group.objects.get_or_create(name='Agency')
        cls.user.groups.add(agency_group)

        cls.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            passport_number='12345',
            date_of_birth='1990-01-01',
            address='123 Main St',
            phone_number='555-1234',
            email='john.doe@example.com',
            agency=cls.user
        )

    def test_employee_str(self):
        self.assertEqual(str(self.employee), 'John Doe')

    def test_employee_is_authenticated(self):
        self.assertTrue(self.employee.is_authenticated)

    def test_employee_is_active(self):
        self.assertTrue(self.employee.is_active)

    def test_employee_is_anonymous(self):
        self.assertFalse(self.employee.is_anonymous)

class EmployeeMemoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        agency_group, created = Group.objects.get_or_create(name='Agency')
        cls.user.groups.add(agency_group)

        cls.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            passport_number='12345',
            date_of_birth='1990-01-01',
            address='123 Main St',
            phone_number='555-1234',
            email='john.doe@example.com',
            agency=cls.user
        )

        cls.memory = EmployeeMemory.objects.create(
            employee=cls.employee,
            note='This is a test note.'
        )

    def test_employee_memory_str(self):
        expected_str = f"Memory for John Doe on {self.memory.created_at.strftime('%Y-%m-%d')}"
        self.assertEqual(str(self.memory), expected_str)
