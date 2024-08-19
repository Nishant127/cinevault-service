from django.urls import path, include

urlpatterns = [
    path("users/", include("users.api.urls"), name="users_api"),
    path("movies/", include("movies.api.urls"), name="movies_api"),
    path(
        "collection/",
        include("movie_collections.api.urls"),
        name="movie_collections_api",
    ),
    path(
        "request-count/",
        include("request_counter.api.urls"),
        name="request_counter_api",
    ),
]
