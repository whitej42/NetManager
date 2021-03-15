from django.urls import include, path
from . import views


urlpatterns = [
    # /device_manager/
    path('', views.device_manager, name='device_manager'),
    path('add-device', views.add_device, name='add_device'),
    path('delete-device', views.delete_device, name='delete_device')
]
