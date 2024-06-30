# agency/tests.py

from django.test import TestCase
from agency.models import Agency

class AgencyModelTest(TestCase):

    def setUp(self):
        self.agency = Agency.objects.create(
            name="Test Agency",
            license_number="12345"
        )

    def test_agency_creation(self):
        """Test if an Agency instance is created correctly."""
        self.assertEqual(self.agency.name, "Test Agency")
        self.assertEqual(self.agency.license_number, "12345")
        self.assertIsNotNone(self.agency.date_created)
        self.assertIsNotNone(self.agency.date_updated)
        self.assertTrue(isinstance(self.agency, Agency))
        self.assertEqual(str(self.agency), "Test Agency")
