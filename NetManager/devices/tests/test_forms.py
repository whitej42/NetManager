"""

DEVICES FORMS UNIT TESTS

"""
from django.test import TestCase
from devices.forms import *


class TestForms(TestCase):

    def test_device_form_valid(self):
        form = DeviceForm(data={
            'name': 'test',
            'type': 'test',
            'host': 'test',
            'vendor': 'test',
            'location': 'test',
            'contact': 'test',
        })
        self.assertTrue(form.is_valid())

    def test_device_form_not_valid(self):
        form = DeviceForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_security_form_valid(self):
        form = SecurityForm(data={
            'username': 'test',
            'password': 'test',
            'secret': 'test',
        })
        self.assertTrue(form.is_valid())

    def test_security_form_not_valid(self):
        form = SecurityForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_interface_form_valid(self):
        form = InterfaceForm(data={
            'interface': 'test',
            'ip_address': 'test',
            'mask': 'test',
            'enable': 'test',   # not required
        })
        self.assertTrue(form.is_valid())

    def test_interface_form_not_valid(self):
        form = InterfaceForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_acl_form_valid(self):
        form = AclForm(data={
            'type': 'standard',
            'name': 'test',
            'statement': 'test',
        })
        self.assertTrue(form.is_valid())

    def test_acl_form_not_valid(self):
        form = AclForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)