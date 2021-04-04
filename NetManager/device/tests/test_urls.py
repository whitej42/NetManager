"""

device url test

"""
from django.test import TestCase
from django.urls import reverse, resolve
from device.views import *
from django.contrib.auth.models import User

from device.models import Device


class TestUrls(TestCase):

    def setUp(self):
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

    def test_device_url(self):
        url = reverse('device', args=[self.device.pk])
        self.assertEqual(resolve(url).func, device_view)

    def test_interface_url(self):
        url = reverse('interface', args=[self.device.pk])
        self.assertEqual(resolve(url).func, interface_view)

    def test_save_config_url(self):
        url = reverse('save_config', args=[self.device.pk])
        self.assertEqual(resolve(url).func, save_config)

    def test_config_interface_url(self):
        actions = ['CONFIG', 'RESET']
        for a in actions:
            url = reverse('config_interface', args=[self.device.pk, a])
            self.assertEqual(resolve(url).func, config_interface)

    def test_access_list_url(self):
        actions = ['CREATE', 'DELETE']
        for a in actions:
            url = reverse('access_list', args=[self.device.pk, a])
            self.assertEqual(resolve(url).func, access_list)

    def test_interface_access_list_url(self):
        actions = ['APPLY', 'REMOVE']
        for a in actions:
            url = reverse('interface_access_list', args=[self.device.pk, a])
            self.assertEqual(resolve(url).func, interface_access_list)

    def test_disable_interfaces_url(self):
        url = reverse('disable_interfaces', args=[self.device.pk])
        self.assertEqual(resolve(url).func, disable_interfaces)