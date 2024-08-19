import pytest
from django.urls import reverse
from rest_framework import status
from movie_collections.models import MovieCollection
import uuid


@pytest.mark.django_db
def test_create_movie_collection(authorized_api_client):
    url = reverse("collection-list")
    data = {
        "title": "Test Collection",
        "description": "A test movie collection",
        "movies": [
            {
                "title": "Test Movie",
                "description": "A test movie",
                "genres": "Action",
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
            }
        ],
    }
    response = authorized_api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert "collection_uuid" in response.data
    assert MovieCollection.objects.filter(
        user=response.wsgi_request.user, title="Test Collection"
    ).exists()


@pytest.mark.django_db
def test_movie_collection_list(authorized_api_client):
    url = reverse("collection-list")
    response = authorized_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "data" in response.data
    assert "collections" in response.data["data"]
    assert "favourite_genres" in response.data["data"]


@pytest.mark.django_db
def test_movie_collection_detail(authorized_api_client, user):
    collection = MovieCollection.objects.create(
        user=user, title="Test Collection", description="A test movie collection"
    )
    collection_uuid = collection.uuid
    url = reverse("collection-deatil", kwargs={"collection_uuid": collection_uuid})
    response = authorized_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "data" in response.data
    assert response.data["data"]["title"] == "Test Collection"


@pytest.mark.django_db
def test_delete_movie_collection(authorized_api_client, user):
    collection = MovieCollection.objects.create(
        user=user,
        title="To be deleted",
        description="This collection will be deleted",
    )
    collection_uuid = collection.uuid
    url = reverse("collection-deatil", kwargs={"collection_uuid": collection_uuid})
    response = authorized_api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not MovieCollection.objects.filter(uuid=collection_uuid).exists()


@pytest.mark.django_db
def test_movie_collection_not_found(authorized_api_client):
    invalid_uuid = str(uuid.uuid4())
    url = reverse("collection-deatil", kwargs={"collection_uuid": invalid_uuid})
    response = authorized_api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "error" in response.data
    assert response.data["error"] == "Collection not found"
