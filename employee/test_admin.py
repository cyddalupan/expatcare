
from django.test import TestCase
import unittest
from django.contrib.auth.models import User, Group
from django.urls import reverse
from employee.models import Employee, FRA, EmployeeMemory
from statement_of_facts.models import StatementOfFacts

class EmployeeAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a superuser
        cls.superuser = User.objects.create_superuser(
            username="testadmin",
            password="testpassword",
            email="testadmin@example.com"
        )

        # Create an agency user
        agency_group, _ = Group.objects.get_or_create(name="Agency")
        cls.agency_user = User.objects.create_user(
            username="testagency",
            password="testpassword",
            email="testagency@example.com",
            is_staff=True
        )
        cls.agency_user.groups.add(agency_group)

        # Create an FRA
        cls.fra = FRA.objects.create(name="Test FRA", agency=cls.agency_user)

        # Create an employee
        cls.employee = Employee.objects.create(
            first_name="Test",
            last_name="Employee",
            passport_number="P1234567A",
            date_of_birth="1990-01-01",
            address="123 Test St",
            phone_number="1234567890",
            email="test@example.com",
            agency=cls.agency_user,
            fra=cls.fra,
            country="PH"
        )

    def setUp(self):
        self.client.login(username="testadmin", password="testpassword")

    def test_employee_list_view(self):
        """
        Test that the employee list view loads for a superuser.
        """
        url = reverse("admin:employee_employee_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_employee_add_view(self):
        """
        Test that the employee add view loads.
        """
        url = reverse("admin:employee_employee_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_employee_change_view(self):
        """
        Test that the employee change view loads.
        """
        url = reverse("admin:employee_employee_change", args=[self.employee.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_employee_search(self):
        """
        Test that the employee admin search works.
        """
        url = reverse("admin:employee_employee_changelist")
        response = self.client.get(url, {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.employee.first_name)

    def test_agency_list_view(self):
        """
        Test that the agency list view loads for a superuser.
        """
        url = reverse("admin:auth_group_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_fra_list_view(self):
        """
        Test that the FRA list view loads for a superuser.
        """
        url = reverse("admin:fra_fra_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_employee_list_view_for_agency(self):
        """
        Test that the employee list view for an agency user only shows their employees.
        """
        self.client.force_login(self.agency_user)

        url = reverse("admin:employee_employee_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.employee.first_name)

        # Create another agency and employee to ensure it's not shown
        other_agency_user = User.objects.create_user(
            username="otheragency",
            password="testpassword",
            email="otheragency@example.com"
        )
        other_agency_user.groups.add(Group.objects.get(name="Agency"))
        other_employee = Employee.objects.create(
            first_name="Other",
            last_name="Employee",
            passport_number="P7654321A",
            date_of_birth="1990-01-01",
            address="456 Other St",
            phone_number="0987654321",
            email="other@example.com",
            agency=other_agency_user,
            country="PH"
        )
        response = self.client.get(url)
        self.assertNotContains(response, other_employee.first_name)

    def test_export_cases(self):
        """
        Test that the export cases view works.
        """
        url = reverse("admin:export_cases")
        response = self.client.get(url, {"employee_id": self.employee.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_generate_statement(self):
        """
        Test that the generate statement of facts view works.
        """
        url = reverse("admin:employee-generate-statement", args=[self.employee.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Test form submission
        response = self.client.post(url, {
            "emotion": "happy",
            "include_consistency_analysis": True,
            "reference_link": "http://example.com",
            "apply": ""
        })
        self.assertEqual(response.status_code, 302) # Redirects on success
        self.assertTrue(StatementOfFacts.objects.filter(employee=self.employee).exists())

    def test_employee_filter_by_fra(self):
        """
        Test filtering employees by FRA.
        """
        url = reverse("admin:employee_employee_changelist")
        response = self.client.get(url, {"fra__id__exact": self.fra.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.employee.first_name)

    def test_employee_filter_by_main_status(self):
        """
        Test filtering employees by main status.
        """
        self.employee.main_status = "with_complain"
        self.employee.save()
        url = reverse("admin:employee_employee_changelist")
        response = self.client.get(url, {"main_status__exact": "with_complain"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.employee.first_name)

    def test_employee_filter_by_applicant_type(self):
        """
        Test filtering employees by applicant type.
        """
        self.employee.applicant_type = "skilled"
        self.employee.save()
        url = reverse("admin:employee_employee_changelist")
        response = self.client.get(url, {"applicant_type__exact": "skilled"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.employee.first_name)

    def test_employee_filter_by_country(self):
        """
        Test filtering employees by country.
        """
        url = reverse("admin:employee_employee_changelist")
        response = self.client.get(url, {"country__exact": "PH"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.employee.first_name)



class EmployeeMemoryAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a superuser
        cls.superuser = User.objects.create_superuser(
            username="testadmin",
            password="testpassword",
            email="testadmin@example.com"
        )

        # Create an agency user
        agency_group, _ = Group.objects.get_or_create(name="Agency")
        cls.agency_user = User.objects.create_user(
            username="testagency",
            password="testpassword",
            email="testagency@example.com"
        )
        cls.agency_user.groups.add(agency_group)

        # Create an employee
        cls.employee = Employee.objects.create(
            first_name="Test",
            last_name="Employee",
            passport_number="P1234567A",
            date_of_birth="1990-01-01",
            address="123 Test St",
            phone_number="1234567890",
            email="test@example.com",
            agency=cls.agency_user,
            country="PH"
        )

        # Create an employee memory
        cls.employee_memory = EmployeeMemory.objects.create(
            employee=cls.employee,
            note="Test memory"
        )

    def setUp(self):
        self.client.login(username="testadmin", password="testpassword")

