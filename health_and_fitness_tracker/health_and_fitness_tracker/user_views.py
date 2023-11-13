from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from app.forms import *
from django.contrib import messages


@login_required(login_url='/')
def HOME(request):
    return render(request, 'User/home.html')


@login_required(login_url='/')
def FOOD_LOG(request):
    food = FoodLog.objects.all()
    categories = FoodCategory.objects.all()
    food_item = FoodItem.objects.all()

    return render(request, 'User/food_log.html', {
        "food": food,
        "categories": categories,
        "food_item": food_item
    })


def log_food(request):
    context = {}  # Initialize an empty context dictionary

    # Fetch all food items from the database
    food_items = FoodItem.objects.all()
    context['food_items'] = food_items  # Add food_items to the context dictionary

    if request.method == "POST":
        form = FoodLogForm(request.POST)
        if form.is_valid():
            food_log = form.save(commit=False)

            # Get the selected food item ID from the form
            food_item_id = request.POST.get('food')
            food_log.food_id = food_item_id

            # Calculate calories consumed based on the selected food item and amount
            # food_log.calories_consumed = food_log.food.calories * food_log.amount_g / 100
            food_log.user = request.user
            food_log.save()
            messages.success(request, 'Food log entry added successfully.')
            return redirect('food_log')
        else:
            messages.error(request, 'Invalid form data. Please check and try again.')
    else:
        form = FoodLogForm()

    context['form'] = form  # Add the form to the context dictionary

    return render(request, 'User/food_log.html', context)

def EXE_LOG(request):
    exercise_logs = ExerciseLog.objects.filter(user=request.user)
    exercise_list = Exercise.objects.all()

    return render(request, 'User/exe_log.html',  {
        "exercise_logs":exercise_logs,
        "exercise_list": exercise_list,
    })

def log_exercise(request):
    context = {}  # Initialize an empty context dictionary

    exercise_list = Exercise.objects.all()
    context['exercise_list'] = exercise_list

    if request.method == "POST":
        form = ExerciseLogForm(request.POST)
        if form.is_valid():
            exercise_log = form.save(commit=False)
            exercise_log.user = request.user
            exercise_log.save()
            messages.success(request, 'Exercise log entry added successfully.')
            return redirect('exe_log')
        else:
            messages.error(request, 'Invalid form data. Please check and try again.')
    else:
        form = ExerciseLogForm()

    context['form'] = form  # Add the form to the context dictionary

    return render(request, 'User/exe_log.html', context)
