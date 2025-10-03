
from django.test import TestCase
from django.contrib.auth.models import User
from fra.models import FRA

class FRAModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.fra = FRA.objects.create(
            name='Test FRA',
            contact='1234567890',
            address='123 Test St',
            country='PH',
            agency=cls.user
        )

    def test_fra_creation(self):
        self.assertEqual(self.fra.name, 'Test FRA')
        self.assertEqual(self.fra.contact, '1234567890')
        self.assertEqual(self.fra.address, '123 Test St')
        self.assertEqual(self.fra.country, 'PH')
        self.assertEqual(self.fra.agency, self.user)

    def test_fra_str(self):
        self.assertEqual(str(self.fra), 'Test FRA')
