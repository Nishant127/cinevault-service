from django.urls import path, include

urlpatterns = [
    path("users/", include("users.api.urls"), name="users_api"),
    path("movies/", include("movies.api.urls"), name="movies_api"),
    path(
        "collection/",
        include("movie_collections.api.urls"),
        name="movie_collections_api",
    ),
]
