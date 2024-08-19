import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import pytest
from rest_framework.test import APIClient
from unittest.mock import patch
from movie_collections.models import MovieCollection
from movies.models import Movie


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
    with patch("movie_collections.api.views.CollectionService") as mock_service:
        yield mock_service

@pytest.fixture
def movie_collection(user):
    collection = MovieCollection.objects.create(
        user=user,
        title="Sample Collection",
        description="A sample movie collection"
    )
    movie = Movie.objects.create(
        uuid="123e4567-e89b-12d3-a456-426614174000",
        title="Sample Movie",
        description="A sample movie",
        genres="Drama"
    )
    collection.movies.add(movie)
    return collection