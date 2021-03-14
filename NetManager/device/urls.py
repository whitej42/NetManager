from django.urls import path
from . import views

urlpatterns = [
    path('<str:device_ID>/', views.get_device, name='device'),
    path('<str:device_ID>/interface-details', views.get_interface, name='interface'),
    path('<str:device_ID>/config-interface', views.config_interface, name='config_interface'),
    path('<str:device_ID>/reset-interface', views.reset_interface, name='reset_interface'),
    path('<str:device_ID>/save-config', views.save_config, name='save_config'),
    path('<str:device_ID>/create-acl', views.create_acl, name='create_acl'),
    path('<str:device_ID>/delete-acl', views.delete_acl, name='delete_acl'),
    path('<str:device_ID>/apply-acl', views.apply_acl, name='apply_acl'),
    path('<str:device_ID>/config-banner', views.config_banner, name='config_banner'),
    path('<str:device_ID>/disable-interfaces', views.disable_interfaces, name='disable_interfaces')
]