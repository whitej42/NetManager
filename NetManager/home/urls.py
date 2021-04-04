from django.urls import path, include
from . import views


urlpatterns = [
    # /home/
    path('', views.home, name='home'),
    path('details/<str:device_ID>/', views.details, name='details'),
    path('reports', views.reports, name='reports'),
    path('add-device', views.add_device, name='add'),
    path('edit-device', views.edit_device, name='edit'),
    path('delete-device', views.delete_device, name='delete'),
    path('update-security', views.update_security, name='security')

]
