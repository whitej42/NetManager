"""

ACCOUNTS URL UNIT TESTS

"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *


class TestUrls(SimpleTestCase):

    def test_index_url(self):
        url = reverse('accounts:Index')
        self.assertEqual(resolve(url).func.view_class, IndexView)

    def test_login_url(self):
        url = reverse('accounts:Login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_profile_url(self):
        url = reverse('accounts:Profile')
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_change_password_url(self):
        url = reverse('accounts:Change-Password')
        self.assertEqual(resolve(url).func, change_password)

    def test_reports_url(self):
        url = reverse('accounts:Reports')
        self.assertEqual(resolve(url).func.view_class, ReportsView)

    def test_help_url(self):
        url = reverse('accounts:Help')
        self.assertEqual(resolve(url).func.view_class, HelpView)