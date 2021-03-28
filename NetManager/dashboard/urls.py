from django.urls import include, path
from . import views

urlpatterns = [
    # /dashboard/
    path('', views.dashboard, name='dashboard'),
    path('details/<str:device_ID>/', views.details, name='details'),
    path('reports', views.reports, name='reports'),
    path('add-device', views.add_device, name='add_device'),
    path('edit-device', views.edit_device, name='edit_device'),
    path('delete-device', views.delete_device, name='delete_device'),
    path('update-secuirty', views.update_security, name='update_security')
]
