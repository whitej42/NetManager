from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    # /
    path('', index_view, name='index'),
    path('login', login_view, name='login'),
    path('profile', profile_view, name='profile'),
    path('profile/update-profile', update_profile, name='update_profile'),
    path('profile/change-password', change_password, name='change_password'),
    path('profile/delete-account', delete_account, name='delete_account'),
    path('reports', reports_view, name='reports'),
    path('help', help_view, name='help'),
]
