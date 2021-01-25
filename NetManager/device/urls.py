from django.urls import path
from . import views

urlpatterns = [
    path('<str:device_ID>/', views.get_device, name='device')
]