from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, FoodItem, FoodCategory
from app.forms import FoodLogForm


def BASE(request):
    return render(request, 'base.html')


def LOGIN(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('user_home')
            elif user_type == '2':
                return HttpResponse('This is Trainer panel')
            else:
                # error message
                messages.error(request, 'Email and Password Are Invalid !')
                return redirect('login')
        else:
            # error message
            messages.error(request, 'Email and Password Are Invalid !')
            return redirect('login')


@login_required(login_url='/')
def doLogout(request):
    logout(request)
    return redirect('login')


def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, 'Your Profile Updated Successfully !')
            return redirect('profile')
        except:
            messages.error(request, 'Failed To Update Your Profile')

    return render(request, 'profile.html')


def log_food(request):
    context = {}  # Initialize an empty context dictionary

    if request.method == "POST":
        form = FoodLogForm(request.POST)
        if form.is_valid():
            food_log = form.save(commit=False)
            # Calculate calories consumed based on the selected food item and amount
            food_log.calories_consumed = food_log.food.calories * food_log.amount_g / 100
            food_log.user = request.user
            food_log.save()
            messages.success(request, 'Food log entry added successfully.')
            return redirect('food_log')
        else:
            messages.error(request, 'Invalid form data. Please check and try again.')
    else:
        form = FoodLogForm()

    # Fetch all food items from the database
    food_items = FoodItem.objects.all()

    context['food_items'] = food_items  # Add food_items to the context dictionary

    return render(request, 'User/food_log.html', context)
