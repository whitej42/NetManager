"""

Accounts views unit tests

"""
from django.test import TestCase, Client
from django.urls import reverse
from test_scripts import test_objects


class TestViews(TestCase):

    """
    Constructor
    * Create test user
    * Set reversed url for each view
    """
    def setUp(self):
        self.client = Client()

        # create test user
        self.user = test_objects.create_test_user(self)

        self.index_url = reverse('accounts:index')
        self.login_url = reverse('accounts:login')
        self.profile_url = reverse('accounts:profile')
        self.reports_url = reverse('accounts:reports')
        self.help_url = reverse('accounts:help')

    def test_index_view(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_view(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_profile_view(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_profile.html')

    def test_update_profile_view(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_profile.html')

    def test_change_password_view(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_profile.html')

    def test_delete_account_view(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_profile.html')

    def test_reports_view(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.reports_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_reports.html')

    def test_help_view(self):
        response = self.client.get(self.help_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_help.html')
