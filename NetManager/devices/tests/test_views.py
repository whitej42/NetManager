"""

// Devices views unit tests


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

        # Test device primary key
        pk = self.device.pk

        # Device Manager View
        self.device_manager_url = reverse('devices:device-manager')
        self.add_device_url = reverse('devices:add-device')

        # Device Details View
        self.device_details_url = reverse('devices:device-details', args=[pk])
        self.save_config_url = reverse('devices:save-config', args=[pk])
        self.config_interface_url = reverse('devices:config-interface', args=[pk])
        self.reset_interface_url = reverse('devices:reset-interface', args=[pk])
        self.disable_interfaces_url = reverse('devices:disable-interfaces', args=[pk])
        self.create_access_list_url = reverse('devices:create-acl', args=[pk])
        self.delete_access_list_url = reverse('devices:delete-acl', args=[pk])
        self.interface_details_url = reverse('devices:interface-details', args=[pk, 'f0/0'])
        self.apply_access_list_url = reverse('devices:apply-acl', args=[pk, 'f0/0'])
        self.remove_access_list_url = reverse('devices:remove-acl', args=[pk, 'f0/0'])

        # Device Settings View
        self.device_settings_url = reverse('devices:device-settings', args=[pk])
        self.delete_device_url = reverse('devices:delete-device', args=[pk])
        self.edit_device_url = reverse('devices:edit-device', args=[pk])
        self.device_security_url = reverse('devices:device-security', args=[pk])

    """
    Test device manager if user logged in
    Assert true - returns device_manager_view
    """
    def test_device_manager_view_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.device_manager_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_manager.html')

    """
    Test device manager if user NOT logged in
    Assert true - returns login_view
    """
    def test_device_manager_view_no_user(self):
        response = self.client.post(self.device_manager_url)
        self.assertRedirects(response, '/accounts/login/?next=/devices/', status_code=302, target_status_code=200)

    """
    Test add device view
    Assert true - returns device_manager_view
    """
    def test_add_device(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.add_device_url)
        self.assertRedirects(response, self.device_manager_url, status_code=302, target_status_code=200)

    """
    Test device details view if device exists and is connected
    Assert true - returns device_details_view
    """
    def test_device_details_view_device_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.device_details_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_details.html')

    """
    Test device details view if device does NOT exists and is NOT connected
    Assert true - returns device_manager_view
    """
    def test_device_details_view_device_not_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('devices:device-details', args=[1]))

        self.assertRedirects(response, self.device_manager_url, status_code=302, target_status_code=200)

    """
    Test save config view if device exists and is connected   
    Assert true - returns device_details_view
    """
    def test_save_config_device_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.save_config_url)

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    """
    Test save config view if device does NOT exists and is NOT connected
    Assert true - returns device_manager_view
    """
    def test_save_config_device_not_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('devices:save-config', args=[1]))

        self.assertRedirects(response, self.device_manager_url, status_code=302,
                             target_status_code=200)

    """
    Test config interface view if device exists and is connected
    Assert true - returns device_details_view
    """
    def test_config_interface_device_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.config_interface_url)

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    """
    Test config interface view if device does NOT exists and is NOT connected
    Assert true - returns device_manager_view
    """
    def test_config_interface_device_not_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('devices:config-interface', args=[1]))

        self.assertRedirects(response, self.device_manager_url, status_code=302,
                             target_status_code=200)

    """
    Test reset interface view if device exists and is connected
    Assert true - returns device_details_view
    """
    def test_reset_interface_device_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.reset_interface_url)

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    """
    Test reset interface view if device does NOT exists and is NOT connected
    Assert true - returns device_manager_view
    """
    def test_reset_interface_device_not_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('devices:reset-interface', args=[1]))

        self.assertRedirects(response, self.device_manager_url, status_code=302,
                             target_status_code=200)

    """
    Test disable interfaces view if device exists and is connected
    Assert true - returns device_details_view
    """
    def test_disable_interfaces_device_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.disable_interfaces_url)

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    """
    Test disable interfaces view if device does NOT exists and is NOT connected
    Assert true - returns device_manager_view
    """
    def test_disable_interfaces_device_not_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('devices:disable-interfaces', args=[1]))

        self.assertRedirects(response, self.device_manager_url, status_code=302,
                             target_status_code=200)

    """
    Test create access list view if device exists and is connected
    Assert true - returns device_details_view
    """
    def test_create_access_list_device_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.create_access_list_url)

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    """
    Test create access list view if device does NOT exists and is NOT connected
    Assert true - returns device_manager_view
    """
    def test_create_access_list_device_not_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('devices:create-acl', args=[1]))

        self.assertRedirects(response, self.device_manager_url, status_code=302,
                             target_status_code=200)

    """
    Test delete access list view if device exists and is connected
    Assert true - returns device_details_view
    """
    def test_delete_access_list_device_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.delete_access_list_url)

        self.assertRedirects(response, self.device_details_url, status_code=302, target_status_code=200)

    """
    Test delete access list view if device does NOT exists and is NOT connected
    Assert true - returns device_manager_view after redirect to device_details
    """
    def test_delete_access_list_device_not_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('devices:delete-acl', args=[1]))

        self.assertRedirects(response, self.device_manager_url, status_code=302,
                             target_status_code=200)

    """
    Test interface details view if device exists and is connected
    Assert true - returns interface_details_view
    """
    def test_interface_details_view_device_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.interface_details_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_interface.html')

    """
    Test interface details view if device does NOT exists and is NOT connected
    Assert true - returns device_manager_view
    """
    def test_interface_details_view_device_not_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('devices:interface-details', args=[1, None]))

        # redirect to device manager
        self.assertRedirects(response, self.device_manager_url, status_code=302,
                             target_status_code=200)

    """
    Test apply access list view if device exists and is connected
    Assert true - returns interface_details_view
    """
    def test_apply_access_list_device_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.apply_access_list_url)

        self.assertRedirects(response, self.interface_details_url, status_code=302, target_status_code=200)

    def test_apply_access_list_device_not_connected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('devices:apply-acl', args=[1, None]))

        # redirect to device manager
        self.assertRedirects(response, self.device_manager_url, status_code=302,
                             target_status_code=200)

    """
    Test device settings view if device exists in database
    Assert true - returns device_settings_view
    """
    def test_device_settings_view_device_exists(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.device_settings_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'device_settings.html')