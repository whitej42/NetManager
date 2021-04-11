"""

DEVICES VIEWS UNIT TESTS


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
            user=self.user,
            name='device_test',
            type='test_device',
            # active device
            host='192.168.0.29',
            vendor='Cisco',
        )

        # Create security object for test device
        self.security = Security.objects.create(
            device=self.device,
            username='admin',
            password='cisco'
        )

        # Test devices primary key
        pk = self.device.pk

        self.device_manager_url = reverse('devices:Device-Manager')
        self.device_details_url = reverse('devices:Device-Details', args=[pk])
        self.interface_details_url = reverse('devices:Interface-Details', args=[pk, 'f0/1'])
        self.device_settings_url = reverse('devices:Device-Settings', args=[pk])
        self.config_view_url = reverse('devices:Device-Config', args=[pk])

    def test_device_manager_view_GET(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.device_manager_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_manager.html')

    def test_device_details_view_GET(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.device_details_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_details.html')

    def test_interface_details_view_GET(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.interface_details_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_interface.html')

    def test_device_settings_view_GET(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.device_settings_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_settings.html')

    def test_config_view_GET(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.config_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_config.html')

    def test_device_manager_add_device_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_manager_url, {
            'name': 'test',
            'type': 'test',
            'host': 'test',
            'vendor': 'test',
            'location': 'test',
            'contact': 'test',
        })

        self.assertRedirects(response, self.device_manager_url, status_code=302, target_status_code=200)

    def test_device_details_save_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_details_url, {
            'save': 'save',
        })

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    def test_device_details_config_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_details_url, {
            'interface': 'test',
            'ip_address': 'test',
            'mask': 'test',
            'enable': 'On',
            'config': 'config',
        })

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    def test_device_details_reset_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_details_url, {
            'reset': 'reset',
        })

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    def test_device_details_disable_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_details_url, {
            'disable': 'disable',
        })

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    def test_device_details_create_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_details_url, {
            'type': 'standard',
            'name': 'test',
            'statement': 'test',
            'create': 'create',
        })

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    def test_device_details_delete_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_details_url, {
            'acl': 'test',
            'delete': 'delete',
        })

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    def test_interface_details_apply_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.interface_details_url, {
            'acl': 'test',
            'dir': 'in',
            'apply': 'apply'
        })

        self.assertRedirects(response, self.interface_details_url, status_code=302, target_status_code=200)

    def test_interface_details_remove_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.interface_details_url, {
            'acl': 'test',
            'dir': 'in',
            'remove': 'remove'
        })

        self.assertRedirects(response, self.interface_details_url, status_code=302, target_status_code=200)

    def test_device_settings_edit_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_settings_url, {
            'name': 'test',
            'type': 'test',
            'host': 'test',
            'vendor': 'test',
            'location': 'test',
            'contact': 'test',
            'edit': 'edit',
        })

        self.assertRedirects(response, self.device_settings_url, status_code=302, target_status_code=200)

    def test_device_settings_security_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_settings_url, {
            'username': 'test',
            'password': 'test',
            'secret': 'test',
            'security': 'security',
        })

        self.assertRedirects(response, self.device_settings_url, status_code=302, target_status_code=200)

    def test_device_settings_delete_POST(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.post(self.device_settings_url, {
            'delete': 'delete',
        })

        self.assertRedirects(response, self.device_manager_url, status_code=302, target_status_code=200)

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
