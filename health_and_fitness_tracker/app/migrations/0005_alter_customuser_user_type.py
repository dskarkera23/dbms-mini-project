# Generated by Django 4.2.7 on 2023-11-26 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_bmilog_log_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('1', 'USER'), ('2', 'TRAINER'), ('3', 'ADMIN')], default=1, max_length=50),
        ),
    ]
