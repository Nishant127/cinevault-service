from rest_framework.views import APIView
from rest_framework import response, status, permissions
from .serializers import (
    MovieCollectionSerializer,
    MovieCollectionListSerializer,
    MovieCollectionDetailSerializer,
    UpdateMovieCollectionSerializer,
)
from movie_collections.service import CollectionService
from movie_collections.models import MovieCollection


class MovieCollectionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        collections = request.user.collections.all()
        serializer = MovieCollectionListSerializer(collections, many=True)
        top_genres = CollectionService.get_top_genres(request.user)
        return response.Response(
            {
                "is_success": True,
                "data": {
                    "collections": serializer.data,
                    "favourite_genres": top_genres,
                },
            }
        )

    def post(self, request):
        try:
            serializer = MovieCollectionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            collection = CollectionService.create_collection(
                serializer.validated_data, request.user
            )
            return response.Response(
                {"collection_uuid": collection.uuid}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return response.Response(
                {"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class MovieCollectionDetailApiView(APIView):
    def get(self, request, **kwargs):
        try:
            collection_uuid = kwargs.get("collection_uuid")
            collection = MovieCollection.objects.get(
                uuid=collection_uuid, user=request.user
            )
            serializer = MovieCollectionDetailSerializer(collection)
            return response.Response({"is_success": True, "data": serializer.data})
        except MovieCollection.DoesNotExist:
            return response.Response(
                {"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return response.Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, **kwargs):
        try:
            collection_uuid = kwargs.get("collection_uuid")
            collection = MovieCollection.objects.get(
                uuid=collection_uuid, user=request.user
            )
            serializer = UpdateMovieCollectionSerializer(
                collection, data=request.data, partial=True
            )
            if serializer.is_valid():
                updated_collection = serializer.save()
            return response.Response(
                {"collection_uuid": updated_collection.uuid}, status=status.HTTP_200_OK
            )
        except MovieCollection.DoesNotExist:
            return response.Response(
                {"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return response.Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, **kwargs):
        try:
            collection_uuid = kwargs.get("collection_uuid")
            collection = MovieCollection.objects.get(
                uuid=collection_uuid, user=request.user
            )
            collection.delete()
            return response.Response(
                {"message": "Collection deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except MovieCollection.DoesNotExist:
            return response.Response(
                {"error": "Collection not found."}, status=status.HTTP_404_NOT_FOUND
            )
