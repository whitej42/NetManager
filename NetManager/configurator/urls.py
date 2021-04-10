from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'config'
urlpatterns = [
    # configurator/
    path('<int:device_id>', login_required(ConfigView.as_view()), name='Config'),
]