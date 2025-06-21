import pytest
from django.urls import reverse
from django.contrib.auth.models import User

# Test that a new user can successfully register via the registration form
@pytest.mark.django_db
# The 'client' is a built-in Django test client provided automatically by pytest-django
def test_user_can_register(client):
    # Get the URL for the registration page using the URL name 'register'
    url = reverse('register')
    
    # Simulate submitting a POST request to the registration page with form data
    response = client.post(url, {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123456789',
        'password_confirm': 'password123456789'
    })

    # Verifies a new User instance with username 'newuser' exists in the database
    assert User.objects.filter(username='newuser').exists()
    
    # Verifies the response status code is 302, indicating a redirect after successful registration
    assert response.status_code == 302