# Generated by Django 4.2.7 on 2023-11-26 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_exercise_calories_burned_per_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciselog',
            name='calories_burned',
            field=models.PositiveIntegerField(default=0),
        ),
    ]