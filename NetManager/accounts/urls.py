from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('', views.create, name='login.html'),
]