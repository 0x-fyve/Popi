from django.shortcuts import render
from .models import Room
import secrets
import string
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

# Create your views here.
def generate_room_code():
    clean_alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    
    # Securely select 6 characters
    code = ''.join(secrets.choice(clean_alphabet) for _ in range(6))

    while Room.objects.filter(code=code).exists():
        code = ''.join(secrets.choice(clean_alphabet) for _ in range(6))

    return code

class CreateRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user= request.user
        code = generate_room_code()

        room = Room.objects.create(code=code, host=user)

        return Response({"code": room.code, "join_url": f"/join/{room.code}", "status": room.status})

class JoinRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")

        room = Room.objects.filter(code=code).first()

        if not room:
            return Response({"error": "Room not found."}, status=404)
        if room.status == "closed":
            return Response({"error": "Room is closed."}, status=400)

        return Response(
            {
                "message": "Successfully joined the room.", 
                "code": room.code,
                "host": {
                    "id": room.host.id,
                    "username": room.host.username,
                },
                "status": room.status
            }, status=200)
