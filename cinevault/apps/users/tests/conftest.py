import pytest
from rest_framework.test import APIClient
from users.tests.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory.create()


@pytest.fixture
def create_user():
    def _create_user(username="testuser", password="password123"):
        return UserFactory.create(username=username, password=password)

    return _create_user
