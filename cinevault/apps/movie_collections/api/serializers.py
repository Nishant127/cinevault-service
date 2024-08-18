from rest_framework import serializers
from movie_collections.models import MovieCollection
from movies.models import Movie
from movie_collections.service import CollectionService


class MovieSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    genres = serializers.CharField(allow_blank=True)
    uuid = serializers.UUIDField()


class MovieCollectionSerializer(serializers.Serializer):
    movies = MovieSerializer(many=True)
    title = serializers.CharField()
    description = serializers.CharField()
