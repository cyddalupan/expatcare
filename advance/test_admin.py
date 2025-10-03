
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django import forms

from advance.models import Setting, AICategory
from advance.forms import AICategoryForm

User = get_user_model()


class AdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.superuser = User.objects.create_superuser(
            username="testadmin",
            email="testadmin@example.com",
            password="testpassword",
        )
        cls.setting1 = Setting.objects.create(
            name="Test Setting 1", value="Test Value 1", value_type="str"
        )
        cls.setting2 = Setting.objects.create(
            name="Test Setting 2", value="Test Value 2", value_type="int"
        )
        cls.aicategory = AICategory.objects.create(
            category_name="Test Category",
            welcome_message="Test Welcome Message",
            closing_message="Test Closing Message",
            role="Test Role",
            function_description="Test Function Description",
        )

    def test_admin_loads(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

    def test_setting_list_view_loads(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.get(reverse("admin:advance_setting_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_aicategory_list_view_loads(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.get(reverse("admin:advance_aicategory_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_setting_create(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.post(
            reverse("admin:advance_setting_add"),
            {"name": "New Setting", "value": "New Value", "value_type": "str"},
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(Setting.objects.filter(name="New Setting").exists())

    def test_setting_update(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.post(
            reverse("admin:advance_setting_change", args=[self.setting1.id]),
            {"name": "Updated Setting", "value": "Updated Value", "value_type": "str"},
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.setting1.refresh_from_db()
        self.assertEqual(self.setting1.name, "Updated Setting")

    def test_setting_delete(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.post(
            reverse("admin:advance_setting_delete", args=[self.setting1.id]), {"post": "yes"}
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertFalse(Setting.objects.filter(id=self.setting1.id).exists())

    def test_setting_search(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.get(
            reverse("admin:advance_setting_changelist"), {"q": "Test Setting 1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Setting 1")
        self.assertNotContains(response, "Test Setting 2")

    def test_setting_filter(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.get(
            reverse("admin:advance_setting_changelist"), {"value_type": "str"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Setting 1")
        self.assertNotContains(response, "Test Setting 2")

    def test_aicategory_create(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.post(
            reverse("admin:advance_aicategory_add"),
            {
                "category_name": "New Category",
                "welcome_message": "New Welcome Message",
                "closing_message": "New Closing Message",
                "role": "New Role",
                "function_description": "New Function Description",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(AICategory.objects.filter(category_name="New Category").exists())

    def test_aicategory_update(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.post(
            reverse("admin:advance_aicategory_change", args=[self.aicategory.id]),
            {
                "category_name": "Updated Category",
                "welcome_message": "Updated Welcome Message",
                "closing_message": "Updated Closing Message",
                "role": "Updated Role",
                "function_description": "Updated Function Description",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.aicategory.refresh_from_db()
        self.assertEqual(self.aicategory.category_name, "Updated Category")

    def test_aicategory_delete(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.post(
            reverse("admin:advance_aicategory_delete", args=[self.aicategory.id]),
            {"post": "yes"},
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertFalse(AICategory.objects.filter(id=self.aicategory.id).exists())

    def test_aicategory_form_in_admin(self):
        self.client.login(username="testadmin", password="testpassword")
        response = self.client.get(
            reverse("admin:advance_aicategory_change", args=[self.aicategory.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["adminform"].form, AICategoryForm)
        self.assertIsInstance(
            response.context["adminform"].form.fields["role"].widget,
            forms.Textarea,
        )
