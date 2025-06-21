from .views import *
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', user_dashboard_view, name='user-dashboard'),
    path('admin-dashboard/', admin_dashboard_view, name='admin-dashboard'),
]
