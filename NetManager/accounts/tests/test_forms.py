"""

ACCOUNTS FORMS UNIT TESTS

"""
from django.test import TestCase
from accounts.forms import *
from test_scripts import test_objects


class TestForms(TestCase):

    def setUp(self):
        # create test user
        self.user = test_objects.create_test_user(self)

    def test_login_form_valid(self):
        form = LoginForm(data={
            'username': self.user.username,
            'password': self.user.password,
        })
        self.assertTrue(form.is_valid())

    def test_login_form_not_valid(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_register_form_is_valid(self):
        form = RegisterForm(data={
            'username': 'test_user',
            'email': 'test@test.com',
            'email2': 'test@test.com',
            'password': 'test'
        })
        self.assertTrue(form.is_valid())

    def test_register_form_not_valid(self):
        form = RegisterForm(data={
            'username': 'test_user',
            'email': 'test@test.com',
            'email2': 'test_1@test.com',
            'password': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_register_form_is_empty(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_profile_form_is_valid(self):
        form = ProfileForm(data={
            'username': 'test_user',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test'
        })
        self.assertTrue(form.is_valid())

    def test_profile_form_not_valid(self):
        form = ProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_change_password_form_is_valid(self):
        form = ChangePasswordForm(data={
            'password': 'test',
            'password2': 'test'
        })
        self.assertTrue(form.is_valid())

    def test_change_password_form_not_valid(self):
        form = ChangePasswordForm(data={
            'password': 'test',
            'password2': 'test1'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_change_password_form_empty(self):
        form = ChangePasswordForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)