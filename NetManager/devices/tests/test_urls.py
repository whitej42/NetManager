"""

DEVICES URL TESTS

"""
from django.test import TestCase
from django.urls import reverse, resolve
from devices.views import *
from test_scripts import test_objects


class TestUrls(TestCase):

    def test_device_manager_url(self):
        url = reverse('devices:device-manager')
        self.assertEqual(resolve(url).func, device_manager_view)

    def test_device_details_url(self):
        url = reverse('devices:device-details', args=[1])
        self.assertEqual(resolve(url).func, device_details_view)

    def test_save_config_url(self):
        url = reverse('devices:save-config', args=[1])
        self.assertEqual(resolve(url).func, save_config)

    def test_config_interface_url(self):
        url = reverse('devices:config-interface', args=[1])
        self.assertEqual(resolve(url).func, config_interface)

    def test_reset_interface_url(self):
        url = reverse('devices:reset-interface',args=[1])
        self.assertEqual(resolve(url).func, reset_interface)

    def test_disable_interfaces_url(self):
        url = reverse('devices:disable-interfaces', args=[1])
        self.assertEqual(resolve(url).func, disable_interfaces)

    def test_create_access_list_url(self):
        url = reverse('devices:create-acl', args=[1])
        self.assertEqual(resolve(url).func, create_access_list)

    def test_delete_access_list_url(self):
        url = reverse('devices:delete-acl', args=[1])
        self.assertEqual(resolve(url).func, delete_access_list)

    def test_interface_details_url(self):
        url = reverse('devices:interface-details', args=[1, None])
        self.assertEqual(resolve(url).func, interface_details_view)

    def test_apply_access_list_url(self):
        url = reverse('devices:apply-acl', args=[1, None])
        self.assertEqual(resolve(url).func, apply_access_list)

    def test_remove_access_list_url(self):
        url = reverse('devices:remove-acl', args=[1, None])
        self.assertEqual(resolve(url).func, remove_access_list)

    def test_device_settings_views(self):
        url = reverse('devices:device-settings', args=[1])
        self.assertEqual(resolve(url).func, device_settings_view)

    def test_delete_device_views(self):
        url = reverse('devices:delete-device', args=[1])
        self.assertEqual(resolve(url).func, delete_device)

    def test_edit_device_views(self):
        url = reverse('devices:edit-device', args=[1])
        self.assertEqual(resolve(url).func, edit_device)