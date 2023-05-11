from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """
    User model
    """

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
