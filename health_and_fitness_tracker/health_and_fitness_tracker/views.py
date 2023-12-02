from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, FoodItem, FoodCategory, FoodLog
from app.forms import FoodLogForm


def BASE(request):
    return render(request, 'base.html')


def LOGIN(request):
    return render(request, 'login.html')

def SIGNUP(request):
    return render(request, 'signup.html')


def doSignup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')  # Use 'password1' from the form for clarity
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')

        try:
            # Create a user instance
            user = CustomUser.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
            )

            # Use set_password to properly hash the password
            user.set_password(password)

            # Alternatively, you can use make_password to hash the password
            # user.password = make_password(password)

            user.save()

            messages.success(request, 'Account created successfully!')
            return redirect('login')
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to create an account. Please try again.')
            return redirect('signup')


def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('dashboard')
            elif user_type == '2':
                return redirect('trainer_dashboard')
            elif user_type == '3':
                return redirect('dashboard')
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


def select_trainer(request):
    if request.method == 'POST':
        selected_trainer_id = request.POST.get('selected_trainer')
        if selected_trainer_id:
            selected_trainer = CustomUser.objects.get(pk=selected_trainer_id)

            # Update the user's selected_trainer field
            request.user.selected_trainer = selected_trainer
            request.user.save()

            # Notify the user and selected trainer (implement your notification logic here)

    # Only fetch trainers for users with user_type '2'
    trainers = CustomUser.objects.filter(user_type='2')

    context = {
        'trainers': trainers,
    }

    # Check if the user already has a selected trainer
    if request.user.selected_trainer:
        context['selected_trainer_name'] = request.user.selected_trainer.get_full_name()
    else:
        context['selected_trainer_name'] = "None"

    return render(request, 'select_trainer.html', context)