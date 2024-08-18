from django.urls import path
from . import views

urlpatterns = [
    path("", views.MovieListAPIView.as_view(), name="movie-list"),
]
