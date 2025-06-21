import pytest
from django.urls import reverse
from django.contrib.auth.models import User

# Tests cover login flow:
# - redirect for regular, staff, superuser users
# - login failure
# - access control for dashboards (authorized/unauthorized)

@pytest.mark.django_db
def test_regular_user_login_redirects_to_user_dashboard(client):
    # Test redirect after login for a normal user
    # Create regular user
    User.objects.create_user(username='newuser', password='password123')
    # Post login credentials
    url = reverse('login')
    response = client.post(url, {
        'username': 'newuser',
        'password': 'password123',
    })
    assert response.status_code == 302
    assert response.url == reverse('user-dashboard')

@pytest.mark.django_db
def test_admin_user_login_redirects_to_admin_dashboard(client):
    # Test redirect after login for staff user
    # Create staff user
    User.objects.create_user(username='adminuser', password='adminpass123', is_staff=True)
    url = reverse('login')
    response = client.post(url, {
        'username': 'adminuser',
        'password': 'adminpass123',
    })
    assert response.status_code == 302
    assert response.url == reverse('admin:index')

@pytest.mark.django_db
def test_superuser_login_redirects_to_admin_dashboard(client):
    # Test redirect after login for superuser
    # Create superuser
    User.objects.create_user(username='superuser', password='superpass123', is_superuser=True)
    url = reverse('login')
    response = client.post(url, {
        'username': 'superuser',
        'password': 'superpass123',
    })
    assert response.status_code == 302
    assert response.url == reverse('admin:index')

@pytest.mark.django_db
def test_login_fails_with_wrong_password(client):
    # Tests login failure with incorrect password
    User.objects.create_user(username='newuser', password='password123')
    url = reverse('login')
    response = client.post(url, {
        'username': 'newuser',
        'password': 'wrongpassword',
    })
    # Login form re-rendered with error
    assert response.status_code == 200
    assert b"Please enter a correct username and password" in response.content

@pytest.mark.django_db
def test_user_dashboard_requires_login(client):
    # Access user dashboard without login redirects to login
    url = reverse('user-dashboard')
    response = client.get(url)
    # Redirects to login page when not logged in
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_logged_in_regular_user_can_access_user_dashboard(client):
    # Regular logged-in user can access user dashboard
    user = User.objects.create_user(username='regular', password='securepassword123')
    client.login(username='regular', password='securepassword123')
    url = reverse('user-dashboard')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_logged_in_admin_user_can_access_admin_dashboard(client):
    # Staff user can access admin dashboard
    admin_user = User.objects.create_user(username='admin', password='securepassword123', is_staff=True)
    client.login(username='admin', password='securepassword123')
    url = reverse('admin:index')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_logged_in_regular_user_cannot_access_admin_dashboard(client):
    # Regular user cannot access admin dashboard, expect 403
    user = User.objects.create_user(username='regular', password='securepassword123')
    client.login(username='regular', password='securepassword123')
    url = reverse('admin:index')
    response = client.get(url)
    assert response.status_code == 403
