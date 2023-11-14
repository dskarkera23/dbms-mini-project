from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from app.forms import *
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone


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

    return render(request, 'User/exe_log.html', {
        "exercise_logs": exercise_logs,
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


def log_bmi(request):
    context = {}

    if request.method == "POST":
        form = BMILogForm(request.POST)
        if form.is_valid():
            bmi_log = form.save(commit=False)
            bmi_log.user = request.user

            if not bmi_log.log_date:
                bmi_log.log_date = timezone.now().date()

            # Calculate BMI
            height_m = bmi_log.height / 100
            bmi_log.bmi = bmi_log.weight / (height_m * height_m)

            bmi_log.save()
            messages.success(request, 'BMI log entry added successfully.')
            return redirect('bmi_log')
        else:
            messages.error(request, 'Invalid form data. Please check and try again.')
    else:
        form = BMILogForm()

    context['form'] = form
    # Retrieve BMI logs for the current user
    context['bmi_logs'] = BMILog.objects.filter(user=request.user)

    return render(request, 'User/bmi_log.html', context)


def dashboard(request):

    bmi_logs = BMILog.objects.filter(user=request.user).order_by('-log_date')[:10]

    log_dates = [log.log_date.strftime('%Y-%m-%d') for log in bmi_logs]
    bmi_values = [log.bmi for log in bmi_logs]



    # Calculate BMI condition for the most recent log
    if bmi_logs:
        latest_bmi = bmi_logs[0].bmi
        bmi_condition = get_bmi_condition(latest_bmi)

    else:
        latest_bmi = None
        bmi_condition = None

    context = {
        'bmi_logs': bmi_logs,
        'latest_bmi': latest_bmi,
        'bmi_condition': bmi_condition,
        'log_dates': log_dates,
        'bmi_values': bmi_values,  # Pass the dynamic BMI values
    }

    return render(request, 'User/home.html', context)


def get_bmi_graph_data(request):
    bmi_logs = BMILog.objects.filter(user=request.user).order_by('log_date')[:10]

    log_dates = [log.log_date.strftime('%Y-%m-%d') for log in bmi_logs]
    bmi_values = [log.bmi for log in bmi_logs]

    # Determine BMI condition for the latest log
    latest_bmi_condition = get_bmi_condition(bmi_logs[0].bmi) if bmi_logs else None

    data = {
        'log_dates': log_dates,
        'bmi_values': bmi_values,
        'latest_bmi_condition': latest_bmi_condition,
    }

    return JsonResponse(data)


def get_bmi_condition(bmi):
    # Implement logic to determine BMI condition based on BMI value
    # You can define your own conditions and thresholds
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 24.9:
        return 'Healthy weight'
    elif 25 <= bmi < 29.9:
        return 'Overweight'
    else:
        return 'Obesity'


def get_bmi_color(condition):
    if condition == "Underweight":
        return "blue"  # Choose your color
    elif condition == "Healthy weight":
        return "green"  # Choose your color
    elif condition == "Overweight":
        return "yellow"  # Choose your color
    else:
        return "red"
