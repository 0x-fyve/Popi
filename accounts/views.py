from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "User created successfully"
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        response.set_cookie(
            key="access_token",
            value=response.data["access"],
            httponly=True,
            samesite='Lax', 
        )

        response.set_cookie(
            key="refresh_token",
            value=response.data["refresh"],
            httponly=True,
            samesite='Lax', 
        )

        del response.data["access"]
        del response.data["refresh"]

        return response



class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "id": request.user.id,
        })    