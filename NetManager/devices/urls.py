"""

File: devices/urls.py

Purpose:
    This code contains the url paths for the devices application

"""

from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


app_name = 'devices'
urlpatterns = [
    # /devices/
    path('', login_required(DeviceManager.as_view()), name='Device-Manager'),

    # /devices/device_id/
    path('<int:device_id>/', login_required(DeviceDetails.as_view()), name='Device-Details'),

    # /devices/device_id/interface/
    path('<int:device_id>/<path:interface>/', login_required(InterfaceDetails.as_view()), name='Interface-Details'),

    # /devices/configurator/device_id/
    path('<int:device_id>/configurator', login_required(DeviceConfig.as_view()), name='Device-Config'),

    # /devices/settings/device_id/
    path('settings/<int:device_id>/', login_required(DeviceSettings.as_view()), name='Device-Settings'),

]
