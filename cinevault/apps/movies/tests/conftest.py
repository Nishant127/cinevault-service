import pytest
from unittest.mock import patch
from movies.service import MovieAPIService
from rest_framework.test import APIClient
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword123')

@pytest.fixture
def token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@pytest.fixture
def authorized_api_client(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.fixture
def mock_movie_api_service():
    with patch("movies.api.views.MovieAPIService") as MockService:
        yield MockService
