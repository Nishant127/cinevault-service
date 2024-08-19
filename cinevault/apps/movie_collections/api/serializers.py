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


class MovieCollectionListSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    uuid = serializers.UUIDField()


class MovieCollectionDetailSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    movies = MovieSerializer(many=True)


class UpdateMovieCollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = MovieCollection
        fields = ["title", "description", "movies"]

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        CollectionService.update_movies(validated_data, instance)
        return instance
