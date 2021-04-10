from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'accounts'
urlpatterns = [
    # /
    path('', IndexView.as_view(), name='Index'),
    path('login', LoginView.as_view(), name='Login'),
    path('profile', login_required(ProfileView.as_view()), name='Profile'),
    path('profile/change-password', change_password, name='Change-Password'),
    path('reports', login_required(ReportsView.as_view()), name='Reports'),
    path('help', HelpView.as_view(), name='Help'),
]
