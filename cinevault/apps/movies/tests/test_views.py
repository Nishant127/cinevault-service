import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import MagicMock


@pytest.mark.django_db
def test_movie_list_success(mock_movie_api_service, authorized_api_client):
    mock_service = mock_movie_api_service.return_value
    mock_service.get_movies.return_value = {
        "count": 1100,
        "results": [
            {"title": "Test Movie", "description": "A test movie", "genres": "Action"}
        ],
        "next": None,
        "previous": None,
    }
    url = reverse("movie-list")
    response = authorized_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Test Movie"
    assert response.data["next"] is None
    assert response.data["previous"] is None


@pytest.mark.django_db
def test_movie_list_unauthorized(api_client):
    url = reverse("movie-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data
    assert response.data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_movie_list_pagination(mock_movie_api_service, authorized_api_client):
    mock_service = mock_movie_api_service.return_value
    mock_service.get_movies.return_value = {
        "results": [
            {
                "title": "Test Movie 1",
                "description": "A test movie 1",
                "genres": "Action",
            },
            {
                "title": "Test Movie 2",
                "description": "A test movie 2",
                "genres": "Comedy",
            },
        ],
        "next": "http://testserver/movies/?page=2",
        "previous": None,
    }
    url = reverse("movie-list")
    response = authorized_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["title"] == "Test Movie 1"
    assert response.data["next"] == "http://testserver/api/v1/movies/?page=2"
    assert response.data["previous"] is None

@pytest.mark.django_db
def test_movie_list_failure(mock_movie_api_service, authorized_api_client):
    mock_service = mock_movie_api_service.return_value
    mock_service.get_movies.return_value = None
    url = reverse("movie-list")
    response = authorized_api_client.get(url)
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "error" in response.data
    assert response.data["error"] == "Failed to fetch movies."