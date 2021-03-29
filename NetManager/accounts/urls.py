from django.urls import include, path
from . import views

urlpatterns = [
    # /home/
    path('', views.index, name='index'),
    path('login', views.sign_in, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/update-profile', views.update_profile, name='update_profile'),
    path('profile/change-password', views.change_password, name='change_password'),
    path('profile/delete-account', views.delete_account, name='delete_account'),
]
