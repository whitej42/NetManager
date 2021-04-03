"""

accounts urls tests

"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *


class TestUrls(SimpleTestCase):

    def test_index_url(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, sign_in)

    def test_profile_url(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)

    def test_update_profile_url(self):
        url = reverse('update_profile')
        self.assertEqual(resolve(url).func, update_profile)

    def test_change_password_url(self):
        url = reverse('change_password')
        self.assertEqual(resolve(url).func, change_password)

    def test_delete_account_url(self):
        url = reverse('delete_account')
        self.assertEqual(resolve(url).func, delete_account)