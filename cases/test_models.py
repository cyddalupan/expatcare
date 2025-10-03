
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Case, CaseComment, Employee
from django.utils import timezone

class CaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.agency = User.objects.create_user('agency', 'agency@test.com', 'password')
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
        cls.case = Case.objects.create(
            employee=cls.employee, 
            category='Test Category', 
            report='Test Report', 
            agency=cls.user
        )
        cls.comment = CaseComment.objects.create(
            case=cls.case, 
            author=cls.user, 
            text='Test comment'
        )

    def test_case_str(self):
        self.assertEqual(str(self.case), 'Test Category - Test User (Open)')

    def test_case_comment_str(self):
        self.assertEqual(str(self.comment), 'Comment by testuser on Test Category')
