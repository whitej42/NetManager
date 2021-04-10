"""

DEVICES TEST FORMS

"""

from django.test import TestCase
from devices.forms import *
from test_scripts import test_objects


class TestForms(TestCase):

    def setUp(self):
        # create test devices
        self.user = test_objects.create_test_user(self)