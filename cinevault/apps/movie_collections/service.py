# services/collection_service.py
from .models import Movie
from movie_collections.models import MovieCollection


class CollectionService:
    @staticmethod
    def create_collection(validated_data, user):
        movies_data = validated_data.pop("movies")
        collection = MovieCollection.objects.create(user=user, **validated_data)
        CollectionService._add_movies_to_collection(collection, movies_data)
        return collection

    @staticmethod
    def _add_movies_to_collection(collection, movies_data):
        for movie_data in movies_data:
            movie, _ = Movie.objects.get_or_create(
                uuid=movie_data.pop("uuid"),
                defaults={
                    "title": movie_data.get("title"),
                    "description": movie_data.get("description"),
                    "genres": movie_data.get("genres"),
                },
            )
            collection.movies.add(movie)
