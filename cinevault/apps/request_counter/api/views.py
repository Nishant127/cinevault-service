from rest_framework.views import APIView
from rest_framework import status, permissions, response
from django.core.cache import cache


class RequestCounterAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            count = cache.get("request_count", 0)
            return response.Response({"requests": count}, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                {"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ResetRequestCounterAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            cache.set("request_count", 0)
            return response.Response(
                {"message": "Request count reset successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return response.Response(
                {"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
