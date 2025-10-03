from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from advance.models import Setting

User = get_user_model()


class SettingViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.setting1 = Setting.objects.create(
            name="Test Setting 1", value="Test Value 1", value_type="str"
        )
        cls.setting2 = Setting.objects.create(
            name="Test Setting 2", value="123", value_type="int"
        )

    def setUp(self):
        pass

    def setUpAuthenticated(self):
        self.client.login(username="testuser", password="testpassword")

    def test_list_settings(self):
        self.setUpAuthenticated()
        url = reverse("setting-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_setting(self):
        self.setUpAuthenticated()
        url = reverse("setting-detail", args=[self.setting1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.setting1.name)

    def test_create_setting(self):
        self.setUpAuthenticated()
        url = reverse("setting-list")
        data = {"name": "New Setting", "value": "New Value", "value_type": "str"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Setting.objects.filter(name="New Setting").exists())

    def test_update_setting(self):
        self.setUpAuthenticated()
        url = reverse("setting-detail", args=[self.setting1.id])
        data = {
            "name": "Updated Setting",
            "value": "Updated Value",
            "value_type": "str",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.setting1.refresh_from_db()
        self.assertEqual(self.setting1.name, "Updated Setting")

    def test_partial_update_setting(self):
        self.setUpAuthenticated()
        url = reverse("setting-detail", args=[self.setting1.id])
        data = {"name": "Patched Setting"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.setting1.refresh_from_db()
        self.assertEqual(self.setting1.name, "Patched Setting")

    def test_delete_setting(self):
        self.setUpAuthenticated()
        url = reverse("setting-detail", args=[self.setting1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Setting.objects.filter(id=self.setting1.id).exists())

    def test_get_by_name(self):
        self.setUpAuthenticated()
        url = reverse("setting-get-by-name", args=[self.setting1.name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.setting1.name)

    def test_get_by_name_not_found(self):
        self.setUpAuthenticated()
        url = reverse("setting-get-by-name", args=["non-existent-setting"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        self.client.logout()

        # List view
        url = reverse("setting-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Detail view
        url = reverse("setting-detail", args=[self.setting1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Create view
        url = reverse("setting-list")
        data = {"name": "New Setting", "value": "New Value", "value_type": "str"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update view
        url = reverse("setting-detail", args=[self.setting1.id])
        data = {
            "name": "Updated Setting",
            "value": "Updated Value",
            "value_type": "str",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Partial update view
        url = reverse("setting-detail", args=[self.setting1.id])
        data = {"name": "Patched Setting"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Delete view
        url = reverse("setting-detail", args=[self.setting1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
