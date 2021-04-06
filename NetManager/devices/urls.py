from django.urls import path
from .views import *

# DEAL WITH CONFIG ONLY

app_name = 'devices'
urlpatterns = [
    # /devices/
    path('', device_manager_view, name='device-manager'),
    path('add-devices', add_device, name='add_device'),

    # /devices/device_id/
    path('<int:device_id>/', device_details_view, name='device-details'),
    path('<int:device_id>/save-config', save_config, name='save-config'),
    path('<int:device_id>/config-interface', config_interface, name='config-interface'),
    path('<int:device_id>/reset-interface', reset_interface, name='reset-interface'),
    path('<int:device_id>/disable-interfaces', disable_interfaces, name='disable-interfaces'),
    path('<int:device_id>/create-access-list', create_access_list, name='create-acl'),
    path('<int:device_id>/delete-access-list', delete_access_list, name='delete-acl'),

    # /devices/device_id/interface/
    path('<int:device_id>/<path:interface>/', interface_details_view, name='interface-details'),
    path('<int:device_id>/<path:interface>/apply-acl', apply_access_list, name='apply-acl'),
    path('<int:device_id>/<path:interface>/remove-acl', remove_access_list, name='remove-acl'),

    # /devices/manager/device_id/
    path('settings/<int:device_id>/', device_settings_view, name='device-settings'),
    path('settings/<int:device_id>/edit-device', edit_device, name='edit-device'),
    path('settings/<int:device_id>/delete-device', delete_device, name='delete-device'),
    path('settings/<int:device_id>/device_security', device_security, name='device-security')

]
