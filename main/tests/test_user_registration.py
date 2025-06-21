import pytest
from django.contrib.auth.models import User
from main.forms import UserRegistrationForm

    
# Test that the custom UserRegistrationForm validates valid data correctly
@pytest.mark.django_db
def test_user_registration_form_valid():
    # Initialize the registration form with valid matching passwords and data
    form = UserRegistrationForm(data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'strongpassword123',
        'password_confirm': 'strongpassword123'
    })
    
    # Assert the form validates successfully
    assert form.is_valid()
    
    # Save the user from the form and assert correct field values
    user = form.save()
    assert user.username == 'newuser'
    assert user.email == 'newuser@example.com'
    assert user.check_password('strongpassword123')
    
# Test that the form correctly rejects submissions where passwords do not match
@pytest.mark.django_db
def test_form_password_mismatch():
    # Initialize the form with mismatching password and confirmation
    form = UserRegistrationForm(data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'strongpassword123',
        'password_confirm': 'different123',
    })
    
    # Assert the form is invalid due to mismatch
    assert not form.is_valid()
    
    # Assert the specific validation error message for password mismatch is present
    assert 'Passwords do not match' in str(form.errors)
    