from django.urls import path
from . import views

urlpatterns = [
    # /device_ID/device/
    path('<str:device_ID>/', views.device_view, name='device'),
    path('<str:device_ID>/interface-details', views.interface_view, name='interface'),
    path('<str:device_ID>/save-config', views.save_config, name='save'),
    path('<str:device_ID>/config-interface', views.config_interface, name='config'),
    path('<str:device_ID>/reset-interface', views.reset_interface, name='reset'),
    path('<str:device_ID>/disable-interfaces', views.disable_interfaces, name='disable'),
    path('<str:device_ID>/create-access-list', views.create_access_list, name='create'),
    path('<str:device_ID>/delete-access-list', views.delete_access_list, name='delete'),
    path('<str:device_ID>/interface-details/apply-access_list', views.apply_access_list, name='apply'),
    path('<str:device_ID>/interface-details/remove-access_list', views.remove_access_list, name='remove'),
]
