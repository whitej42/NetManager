"""

ACCOUNTS URL TESTS

"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *


class TestUrls(SimpleTestCase):

    def test_index_url(self):
        url = reverse('accounts:index')
        self.assertEqual(resolve(url).func, index_view)

    def test_login_url(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func, login_view)

    def test_profile_url(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func, profile_view)

    def test_update_profile_url(self):
        url = reverse('accounts:update_profile')
        self.assertEqual(resolve(url).func, update_profile)

    def test_change_password_url(self):
        url = reverse('accounts:change_password')
        self.assertEqual(resolve(url).func, change_password)

    def test_delete_account_url(self):
        url = reverse('accounts:reports')
        self.assertEqual(resolve(url).func, reports_view)

    def test_help_view(self):
        url = reverse('accounts:help')
        self.assertEqual(resolve(url).func, help_view)