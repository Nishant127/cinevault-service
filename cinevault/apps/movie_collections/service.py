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

    @staticmethod
    def get_top_genres(user):
        genres_count = {}
        for collection in user.collections.all():
            for movie in collection.movies.all():
                genres = movie.genres.split(",")
                for genre in genres:
                    genres_count[genre] = genres_count.get(genre, 0) + 1
        genres_count.pop("", None)
        sorted_genres = sorted(
            genres_count.items(), key=lambda item: item[1], reverse=True
        )
        top_genres = [genre for genre, _ in sorted_genres[:3]]
        return ", ".join(top_genres)

    @classmethod
    def update_movies(cls, validated_data, movie_collection_object):
        movies_data = validated_data.get("movies", [])
        if movies_data:
            instance_existing_movies = movie_collection_object.movies.values_list(
                "uuid", flat=True
            )
            cls.append_new_movies(
                movies_data, movie_collection_object, instance_existing_movies
            )
            cls.remove_old_movies(
                movies_data, movie_collection_object, instance_existing_movies
            )

    @classmethod
    def append_new_movies(
        cls, movies_data, movie_collection_object, instance_existing_movies
    ):
        all_existing_movie_objects = Movie.objects.all()
        new_movies = []
        for movie_data in movies_data:
            movie_uuid = movie_data.get("uuid")
            if movie_uuid not in instance_existing_movies:
                if movie_uuid not in all_existing_movie_objects.values_list(
                    "uuid", flat=True
                ):
                    movie = Movie.objects.create(**movie_data)
                else:
                    movie = all_existing_movie_objects.get(uuid=movie_uuid)
                new_movies.append(movie)
        movie_collection_object.movies.add(*new_movies)

    @classmethod
    def remove_old_movies(
        cls, movies_data, movie_collection_object, instance_existing_movies
    ):
        new_movie_uuids = set(movie_data.get("uuid") for movie_data in movies_data)
        existing_movie_uuids = set(instance_existing_movies)
        uuids_to_delete = existing_movie_uuids - new_movie_uuids
        removed_movies = Movie.objects.filter(uuid__in=uuids_to_delete)
        movie_collection_object.movies.remove(*removed_movies)
