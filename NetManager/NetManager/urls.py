from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('login/', include('accounts.urls')),
    path('device/', include('device.urls')),
    path('help/', include('help.urls')),
    path('device-manager/', include('devicemanager.urls')),
]
