"""

device views test

"""
from django.test import TestCase, Client
from django.urls import reverse
from device.models import *
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User(username=self.username, password=self.password)
        self.user.set_password(self.password)
        self.user.save()

        # create test device
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

        self.device_url = reverse('device', args=[self.device.pk])

    # requires connection to device
    # test device exists and is connected
    def test_device_view_device_exists(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.device_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device.html')

