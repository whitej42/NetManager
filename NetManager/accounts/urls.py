from django.urls import include, path
from . import views

urlpatterns = [
    # /home/
    path('', views.index, name='index'),
    path('login', views.signin, name='login'),
]