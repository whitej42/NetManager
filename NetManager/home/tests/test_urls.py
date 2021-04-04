"""

home url test

"""
from django.test import TestCase
from django.urls import reverse, resolve
from home.views import *
from django.contrib.auth.models import User


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

    def test_main_url(self):
        url = reverse('main')
        self.assertEqual(resolve(url).func, main)

    def test_details_url(self):
        url = reverse('details', args=[self.device.pk])
        self.assertEqual(resolve(url).func, details)

    def test_reports_url(self):
        url = reverse('reports')
        self.assertEqual(resolve(url).func, reports)

    def test_add_device_url(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func, add_device)

    def test_edit_device_url(self):
        url = reverse('edit')
        self.assertEqual(resolve(url).func, edit_device)

    def test_delete_device_url(self):
        url = reverse('delete')
        self.assertEqual(resolve(url).func, delete_device)

    def test_update_security_url(self):
        url = reverse('security')
        self.assertEqual(resolve(url).func, update_security)