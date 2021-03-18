from django.urls import include, path
from . import views


urlpatterns = [
    # /device-manager/
    path('', views.device_manager, name='device_manager'),
    path('add-device', views.add_device, name='add_device'),
    path('delete-device', views.delete_device, name='delete_device'),
    path('edit-device', views.edit_device, name='edit_device'),
]
