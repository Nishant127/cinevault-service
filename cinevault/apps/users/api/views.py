from rest_framework.views import APIView
from rest_framework import status, response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return response.Response(
                {"access_token": access_token}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return response.Response(
                {"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if not user:
                raise Exception("Invalid Credentials")
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            return response.Response(
                {"access_token": access_token}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return response.Response(
                {"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )