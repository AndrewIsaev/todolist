from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    class Sex(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "W", _("Female")

    sex = models.CharField(max_length=1, choices=Sex.choices, default=Sex.MALE)
