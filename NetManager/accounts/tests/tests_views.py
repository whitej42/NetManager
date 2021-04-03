"""

accounts views test

"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User(username=self.username, password=self.password)
        self.user.set_password(self.password)
        self.user.save()

        self.index_url = reverse('index')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')

    def test_index_view(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_sign_in_view(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    # login required
    def test_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    # login required
    def test_update_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    # login required
    def test_change_password_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    # login required
    def test_delete_account_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
