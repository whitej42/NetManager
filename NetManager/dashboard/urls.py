from django.urls import include, path
from . import views


urlpatterns = [
    # /dashboard/
    path('<str:username>/', views.dashboard, name='dashboard'),
    path('reports', views.reports, name='reports')
]
