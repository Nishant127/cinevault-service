import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_registration(api_client):
    registration_url = reverse("user-registration")
    registration_data = {"username": "testuser", "password": "testpassword123"}
    registration_response = api_client.post(
        registration_url, registration_data, format="json"
    )

    assert registration_response.status_code == status.HTTP_201_CREATED
    assert "access_token" in registration_response.data
    assert registration_response.data["access_token"] is not None


@pytest.mark.django_db
def test_login(api_client, create_user):
    user = create_user(username="testuser", password="testpassword123")
    login_url = reverse("user-login")
    login_data = {"username": "testuser", "password": "testpassword123"}
    login_response = api_client.post(login_url, login_data, format="json")
    assert login_response.status_code == status.HTTP_200_OK
    assert "access_token" in login_response.data
    assert login_response.data["access_token"] is not None


@pytest.mark.django_db
def test_login_with_invalid_credentials(api_client):
    login_url = reverse("user-login")
    invalid_login_data = {"username": "nonexistentuser", "password": "wrongpassword"}
    response = api_client.post(login_url, invalid_login_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "errors" in response.data
