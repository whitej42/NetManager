from django.urls import path
from . import views

urlpatterns = [
    path('<str:device_ID>/', views.device, name='device'),
    path('<str:device_ID>/interface-details', views.interface, name='interface'),
    path('<str:device_ID>/save-config', views.save_config, name='save_config'),
    path('<str:device_ID>/config-interface/<str:action>', views.config_interface, name='config_interface'),
    path('<str:device_ID>/access_list/<str:action>', views.access_list, name='access_list'),
    path('<str:device_ID>/interface_access_list/<str:action>', views.interface_access_list, name='interface_access_list'),
    path('<str:device_ID>/disable-interfaces', views.disable_interfaces, name='disable_interfaces'),
]
