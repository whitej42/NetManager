from django.urls import include, path
from . import views

urlpatterns = [
    # /login/
    path('', views.login, name='login'),
    path('', views.create, name='create'),
]