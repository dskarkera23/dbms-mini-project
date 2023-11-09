from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER = (
        (1, 'USER'),
        (2, 'TRAINER'),
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)

