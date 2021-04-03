from django.test import TestCase
from device.models import *


class TestModels(TestCase):

    def setUp(self):
        self.Device = Device.objects.create(
            user='test',
            name='device_test',
            type='test_device',
            host='192.168.0.2',
            vendor='Cisco',
            location='',
            contact='',
            username='',
            password='',
            status='',
        )