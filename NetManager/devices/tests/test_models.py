"""

DEVICES MODELS UNIT TESTS

"""
from django.test import TestCase
from devices.models import *
from django.contrib.auth.models import User


class TestModels(TestCase):
    """
    Constructor
    * Create test user
    * Create test device
    * Create security object for test device
    """
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User(username=self.username, password=self.password)
        self.user.set_password(self.password)
        self.user.save()

        # create test device
        self.device = Device.objects.create(
            user=self.user,
            name='device_test',
            type='test_device',
            host='test',
            vendor='Cisco',
        )

        # Create security object for test device
        self.security = Security.objects.create(
            device=self.device,
            username='test',
            password='test'
        )

    def test_get_device(self):
        func = Device.get_device(self.device.pk)
        self.assertEqual(func, self.device)

    def test_get_device_security(self):
        func = Security.get_device_security(self.device)
        self.assertEqual(func, self.security)

    def test_get_username(self):
        func = Security.get_username(self.device)
        self.assertEqual(func, self.security.username)

    def test_get_password(self):
        func = Security.get_password(self.device)
        self.assertEqual(func, self.security.password)

    def test_get_secret(self):
        func = Security.get_secret(self.device)
        self.assertEqual(func, self.security.secret)
