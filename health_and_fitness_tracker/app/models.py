from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER = (
        ('1', 'USER'),
        ('2', 'TRAINER'),
        ('3', 'ADMIN')
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)
    
    selected_trainer = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients', 
        default=None,
        limit_choices_to={'user_type': '1'}
    )


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
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, null=True, blank=True)
    log_date = models.DateField()
    qty = models.PositiveIntegerField()
    calories_consumed = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}'s Food Log"


class ExerciseCategory(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ExerciseCategory, on_delete=models.CASCADE)
    calories_burned_per_set = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class ExerciseLog(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.PositiveIntegerField()
    sets = models.PositiveIntegerField()
    log_date = models.DateField()
    calories_burned = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Exercise Log"


class BMILog(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='bmi_records')
    height = models.DecimalField(max_digits=5, decimal_places=2)  
    weight = models.DecimalField(max_digits=5, decimal_places=2)  
    bmi = models.DecimalField(max_digits=5, decimal_places=2)  
    log_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.log_date}'

    def get_bmi_condition(self):
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 24.9:
            return 'Healthy weight'
        elif 24.9 <= self.bmi < 29.9:
            return 'Overweight'
        else:
            return 'Obesity'


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'

    @classmethod
    def create_message(cls, sender, receiver, content):
        return cls.objects.create(sender=sender, receiver=receiver, content=content)
