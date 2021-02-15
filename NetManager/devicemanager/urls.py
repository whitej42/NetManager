from django.urls import include, path
from . import views


urlpatterns = [
    # /device_manager/
    path('', views.device_manager, name='device_manager'),
]
