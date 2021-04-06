"""

devices views test

"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from devices.models import Device


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User(username=self.username, password=self.password)
        self.user.set_password(self.password)
        self.user.save()

        # create test devices
        self.device = Device.objects.create(
            pk=1,
            user=self.user,
            name='device_test',
            type='test_device',
            host='',
            vendor='Cisco',
            location='',
            contact='',
            username='',
            password='',
            status=False,
        )

        self.device_url = reverse('devices', args=[self.device.pk])

    # requires connection to devices
    # test devices exists and is connected
    def test_device_view_device_exists(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.device_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_details.html')

