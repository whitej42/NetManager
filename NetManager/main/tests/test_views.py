"""

main views test

"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from device.models import Device


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User(username=self.username, password=self.password)
        self.user.set_password(self.password)
        self.user.save()

        # create test device for urls
        self.device = Device.objects.create(
            pk=1,
            user=self.user,
            name='device_test',
            type='test_device',
            host='192.168.0.2',
            vendor='Cisco',
            location='',
            contact='',
            username='',
            password='',
            status=False,
        )

        self.main_url = reverse('main')
        self.details_url = reverse('details', args=[self.device.pk])
        self.reports_url = reverse('reports')

    def test_main_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.main_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_details_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.details_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')

    def test_reports_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.reports_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports.html')

