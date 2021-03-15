from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('device/', include('device.urls')),
    path('help/', include('help.urls')),
    path('device-manager/', include('manager.urls')),
]
