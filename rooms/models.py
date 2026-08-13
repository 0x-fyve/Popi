from django.db import models
import uuid
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
class RoomStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    EXPIRED = "expired", "Expired"

class Room(models.Model):
    code = models.CharField(max_length=8, unique=True)
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hosted_rooms",
    )
    status = models.CharField(
        max_length=10,
        choices=RoomStatus.choices,
        default=RoomStatus.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    
