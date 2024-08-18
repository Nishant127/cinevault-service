from django.urls import path
from . import views

urlpatterns = [
    path("", views.MovieCollectionAPIView.as_view(), name="collection-list"),
]
