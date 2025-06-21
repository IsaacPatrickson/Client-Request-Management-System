"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.shortcuts import redirect
from main.views import CustomLoginView
from main.admin import custom_admin_site  # Import your custom admin

# Redirect /admin/login/ to your custom login page
def redirect_admin_login(request):
    return redirect('/login/')

urlpatterns = [
    # Redirect non-staff users hitting admin login
    path('admin/login/', redirect_admin_login),

    # Custom login view
    path('login/', CustomLoginView.as_view(), name='login'),

    # App-specific URLs
    path('', include('main.urls')),

    # Use custom admin with permission override
    path('admin/', custom_admin_site.urls),
]
