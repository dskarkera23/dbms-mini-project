from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class UserModel(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', "last_name", "is_staff", "user_type",'selected_trainer',
    )
    fieldsets = (
        (
            None, {
                'fields': ('username', 'password')
            }
        ),
        (
            'Personal Info', {
                'fields': ('first_name', "last_name", "email")
            }
        ),
        (
            'Important dates', {
                'fields': ('last_login',)
            }
        ),
        (
            'Additional Info', {
                'fields': ('user_type',)
            }
        ),
        ('Trainer Info', {
            'fields': ('selected_trainer',),
            }
        ),
    )


admin.site.register(CustomUser, UserModel)
admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(FoodLog)
admin.site.register(ExerciseCategory)
admin.site.register(Exercise)
admin.site.register(ExerciseLog)
admin.site.register(BMILog)
admin.site.register(Message)
