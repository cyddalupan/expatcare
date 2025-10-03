
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Case
from employee.models import Employee

class CaseAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        cls.agency = User.objects.create_user('agency', 'agency@test.com', 'password')
        cls.employee = Employee.objects.create(
            first_name='Test',
            last_name='Employee',
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
        cls.case = Case.objects.create(employee=cls.employee, category='Test Category', report='Test Report', agency=cls.user)

    def setUp(self):
        self.client.login(username='admin', password='password')

    def test_case_admin_list_view(self):
        url = reverse('admin:cases_case_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_case_admin_add_view(self):
        url = reverse('admin:cases_case_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_case_admin_change_view(self):
        url = reverse('admin:cases_case_change', args=[self.case.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_case_admin_delete_view(self):
        url = reverse('admin:cases_case_delete', args=[self.case.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
