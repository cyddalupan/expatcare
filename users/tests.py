from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User
from users.admin import UserAdmin

class UserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(email='super@example.com', password='superpass123')
        self.assertEqual(superuser.email, 'super@example.com')
        self.assertTrue(superuser.check_password('superpass123'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

class CustomUserCreationFormTest(TestCase):
    def test_custom_user_creation_form_valid(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'type': 1,
            'agency': None,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_invalid(self):
        form_data = {
            'email': 'invalid-email',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'type': 1,
            'agency': None,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

class CustomUserChangeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')

    def test_custom_user_change_form_valid(self):
        form_data = {
            'email': 'newtest@example.com',
            'type': 2,
            'agency': None,
        }
        form = CustomUserChangeForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newtest@example.com')

class UserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user_admin = UserAdmin(User, self.site)
        self.client = self.client
        self.superuser = User.objects.create_superuser(email='admin@example.com', password='adminpass123')

    def test_user_admin_list_display(self):
        self.assertEqual(self.user_admin.list_display, ('email', 'type', 'is_staff', 'is_superuser'))

    def test_user_admin_list_filter(self):
        self.assertEqual(self.user_admin.list_filter, ('is_staff', 'is_superuser', 'type'))

    def test_user_admin_fieldsets(self):
        self.assertEqual(
            self.user_admin.fieldsets,
            (
                (None, {'fields': ('email', 'password')}),
                ('Personal info', {'fields': ('type', 'agency', 'date_created', 'last_login')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            )
        )

    def test_admin_view(self):
        self.client.login(email='admin@example.com', password='adminpass123')
        url = reverse('admin:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
