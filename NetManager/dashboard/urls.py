from django.urls import include, path
from . import views

urlpatterns = [
    # /dashboard/
    path('', views.index, name='index'),
    # /dashboard/deviceID/
    path('<str:device_ID>/', views.device, name='device')
]
