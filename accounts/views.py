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

class LogoutView(APIView):
    def post(self, request):
        response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response    



class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "id": request.user.id,
        })    

from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
@ensure_csrf_cookie
def csrf_token(request):
    return Response({"message": "CSRF cookie set"})    

from http.cookies import SimpleCookie
def get_access_token(scope):
    cookie_header = get_cookie_header(scope)

    if not cookie_header:
        return None

    cookie = SimpleCookie()
    cookie.load(cookie_header)

    access_token = cookie.get("access_token")

    return access_token.value if access_token else None

