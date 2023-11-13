from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class UserModel(UserAdmin):
    list_display = ['username', 'user_type']


admin.site.register(CustomUser,UserAdmin)
admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(FoodLog)
admin.site.register(ExerciseCategory)
admin.site.register(Exercise)
admin.site.register(ExerciseLog)
