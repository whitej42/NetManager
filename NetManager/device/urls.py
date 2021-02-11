from django.urls import path
from . import views

urlpatterns = [
    path('<str:device_ID>/', views.get_device, name='device'),
    path('<str:device_ID>/config-interface', views.config_interface, name='config_interface'),
    path('<str:device_ID>/reset-interface', views.reset_interface, name='reset_interface'),
    path('<str:device_ID>/save-config', views.save_config, name='save_config'),
]