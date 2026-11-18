from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *

# Create your views here.
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            RefreshToken(request.data['refresh']).blacklist()
        except (KeyError, TokenError):
            return Response(
                {'detail': "Yaroqsiz yoki yuborilmagan refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_205_RESET_CONTENT)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]