
from django.contrib.auth.models import User, Group
from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.urls import reverse

from fra.models import FRA
from fra.admin import FRAAdmin

class FRAAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.site = AdminSite()
        cls.admin = FRAAdmin(FRA, cls.site)

        cls.super_user = User.objects.create_superuser(username='admin', password='password')
        cls.agency_user = User.objects.create_user(username='agency', password='password')
        agency_group, _ = Group.objects.get_or_create(name='Agency')
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(FRA)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['view_fra', 'add_fra', 'change_fra']
        )
        agency_group.permissions.add(*permissions)
        cls.agency_user.groups.add(agency_group)

        cls.fra1 = FRA.objects.create(name='FRA One', contact='111', country='PH', agency=cls.agency_user)
        cls.fra2 = FRA.objects.create(name='FRA Two', contact='222', country='US', agency=cls.super_user)

    def test_list_view_as_superuser(self):
        self.client.login(username='admin', password='password')
        url = reverse('admin:fra_fra_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FRA One')
        self.assertContains(response, 'FRA Two')

    def test_list_view_as_agency(self):
        self.client.login(username='agency', password='password')
        url = reverse('admin:fra_fra_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FRA One')
        self.assertNotContains(response, 'FRA Two')

    def test_search(self):
        self.client.login(username='admin', password='password')
        url = reverse('admin:fra_fra_changelist')
        response = self.client.get(url, {'q': 'One'})
        self.assertContains(response, 'FRA One')
        self.assertNotContains(response, 'FRA Two')

    def test_filter(self):
        self.client.login(username='admin', password='password')
        url = reverse('admin:fra_fra_changelist')
        response = self.client.get(url, {'country__exact': 'US'})
        self.assertNotContains(response, 'FRA One')
        self.assertContains(response, 'FRA Two')


    def test_add_view(self):
        self.client.login(username='admin', password='password')
        url = reverse('admin:fra_fra_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_change_view(self):
        self.client.login(username='admin', password='password')
        url = reverse('admin:fra_fra_change', args=[self.fra1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_fra(self):
        self.client.login(username='admin', password='password')
        url = reverse('admin:fra_fra_add')
        data = {
            'name': 'New FRA',
            'contact': '333',
            'address': '333 Test St',
            'country': 'CA',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FRA.objects.filter(name='New FRA').exists())

    def test_change_fra(self):
        self.client.login(username='admin', password='password')
        url = reverse('admin:fra_fra_change', args=[self.fra1.pk])
        data = {
            'name': 'FRA One Updated',
            'contact': self.fra1.contact,
            'address': self.fra1.address,
            'country': self.fra1.country,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.fra1.refresh_from_db()
        self.assertEqual(self.fra1.name, 'FRA One Updated')
