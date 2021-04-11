"""

ACCOUNTS VIEWS UNIT TESTS

"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestViews(TestCase):
    """
    Constructor
    * Create test user
    * Set reversed url for each view
    """
    def setUp(self):
        self.client = Client()

        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User(username=self.username, password=self.password)
        self.user.set_password(self.password)
        self.user.save()

        self.index_url = reverse('accounts:Index')
        self.login_url = reverse('accounts:Login')
        self.profile_url = reverse('accounts:Profile')
        self.reports_url = reverse('accounts:Reports')
        self.help_url = reverse('accounts:Help')

    """
    Testing view GET methods
    """
    def test_index_view_GET(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_profile_view_GET(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_profile.html')

    def test_reports_view_GET(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.reports_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_reports.html')

    def test_help_view_GET(self):
        response = self.client.get(self.help_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_help.html')

    """
    Testing view POST methods
    """
    def test_login_view_POST(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })

        self.assertRedirects(response, '/devices/', status_code=302, target_status_code=200)

    def test_profile_view_update_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.profile_url, {
            'username': 'test_user',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'update': 'update'
        })

        self.assertRedirects(response, self.profile_url, status_code=302, target_status_code=200)

    def test_profile_view_delete_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.profile_url, {
            'delete': 'delete'
        })

        self.assertRedirects(response, self.index_url, status_code=302, target_status_code=200)

    def test_change_password_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.profile_url, {
            'password': 'new_password'
        })

        self.assertRedirects(response, self.index_url, status_code=302, target_status_code=200)