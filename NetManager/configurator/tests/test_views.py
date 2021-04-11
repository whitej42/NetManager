"""

CONFIGURATOR VIEWS UNIT TESTS


"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from devices.models import Device, Security


class TestViews(TestCase):
    """
    Constructor
    * Create test user
    * Create test device - Device must be connected!
    * Create security object for test device
    * Set reversed url for each view
    """
    def setUp(self):
        # Create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User(username=self.username, password=self.password)
        self.user.set_password(self.password)
        self.user.save()

        # Create test device
        self.device = Device.objects.create(
            pk=2,
            user=self.user,
            name='device_test',
            type='test_device',
            # active device
            host='192.168.0.29',
            vendor='Cisco',
            location='',
            contact='',
            status=False,
        )

        # Create security object for test device
        self.security = Security.objects.create(
            pk=1,
            device=self.device,
            username='admin',
            password='cisco'
        )

        # Test devices primary key
        pk = self.device.pk

        self.config_view_url = reverse('config:Config', args=[pk])

    def test_config_view_GET(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.config_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_config.html')

    def test_config_view_show_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.config_view_url, {
            'txt_show': 'test',
            'show': 'show',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_config.html')

    def test_config_view_send_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.config_view_url, {
            'txt_config': 'test',
            'send': 'send',
        })

        self.assertRedirects(response, self.config_view_url, status_code=302, target_status_code=200)
