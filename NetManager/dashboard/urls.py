from django.urls import include, path
from . import views


urlpatterns = [
    # /dashboard/
    path('', views.index, name='index'),
]
