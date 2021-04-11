"""

DEVICES URLS UNIT TESTS

"""
from django.test import TestCase
from django.urls import reverse, resolve
from devices.views import *


class TestUrls(TestCase):

    def test_device_manager_url(self):
        url = reverse('devices:Device-Manager')
        self.assertEqual(resolve(url).func.view_class, DeviceManager)

    def test_device_details_url(self):
        url = reverse('devices:Device-Details', args=[1])
        self.assertEqual(resolve(url).func.view_class, DeviceDetails)

    def test_interface_details_url(self):
        url = reverse('devices:Interface-Details', args=[1, 'f0/1'])
        self.assertEqual(resolve(url).func.view_class, InterfaceDetails)

    def test_device_settings_url(self):
        url = reverse('devices:Device-Settings', args=[1])
        self.assertEqual(resolve(url).func.view_class, DeviceSettings)