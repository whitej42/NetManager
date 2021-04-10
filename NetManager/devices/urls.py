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

    # /devices/manager/device_id/
    path('settings/<int:device_id>/', login_required(DeviceSettings.as_view()), name='Device-Settings'),

]
