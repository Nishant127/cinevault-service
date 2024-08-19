from rest_framework.views import APIView
from rest_framework import status, response, permissions
from movies.service import MovieAPIService
from django.urls import reverse


class MovieListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            movie_sevice = MovieAPIService()
            movies_data = movie_sevice.get_movies(page=int(page))
            if movies_data is None:
                return response.Response(
                    {"error": "Failed to fetch movies."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            movies_data["next"] = (
                f"{self.request.build_absolute_uri(reverse('movie-list'))}?page={int(page) + 1}"
                if movies_data["next"]
                else None
            )

            movies_data["previous"] = (
                f"{self.request.build_absolute_uri(reverse('movie-list'))}?page={int(page) - 1}"
                if movies_data["previous"]
                else None
            )
            return response.Response(movies_data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                {"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
