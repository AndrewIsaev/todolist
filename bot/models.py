from django.db import models
from django.utils.crypto import get_random_string
from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    verification_code = models.CharField(
        max_length=50, null=True, blank=True, default=None
    )

    @staticmethod
    def generate_verification_code():
        return get_random_string(length=50)
