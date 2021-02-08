from django.urls import include, path
from . import views

urlpatterns = [
    # /help/
    path('', views.help_page, name='help'),
]