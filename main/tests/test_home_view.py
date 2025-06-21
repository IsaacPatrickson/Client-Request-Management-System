import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_home_view_renders(client):
    url = reverse('home')
    response = client.get(url)

    assert response.status_code == 200
    assert b"<h1>Welcome to the Homepage!" in response.content # A marker from my template