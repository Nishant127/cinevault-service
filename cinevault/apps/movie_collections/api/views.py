from rest_framework.views import APIView
from rest_framework import response, status, permissions
from .serializers import MovieCollectionSerializer
from movie_collections.service import CollectionService


class MovieCollectionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
