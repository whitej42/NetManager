from django.urls import path
from .views import *

app_name = 'config'
urlpatterns = [
    # configurator/
    path('<int:device_id>', configurator_view, name='config'),
    path('<int:device_id>/show-command', show_command, name='show'),
    path('<int:device_id>/send-config', send_config, name='send-config'),
]