from django.urls import path
from . import views

urlpatterns = [
    # /main/
    path('', views.main, name='main'),
    path('details/<str:device_ID>/', views.details, name='details'),
    path('reports', views.reports, name='reports'),
    path('add-device', views.add_device, name='add_device'),
    path('edit-device', views.edit_device, name='edit_device'),
    path('delete-device', views.delete_device, name='delete_device'),
    path('update-security', views.update_security, name='update_security')
]
