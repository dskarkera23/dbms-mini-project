from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER = (
        (1, 'USER'),
        (2, 'TRAINER'),
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)


class Catalog: from django.db import models


class FoodCategory(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    calories = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class FoodLog(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    log_date = models.DateField()
    amount_g = models.PositiveIntegerField()
    calories_consumed = models.PositiveIntegerField()
