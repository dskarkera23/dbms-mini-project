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
        password = request.POST.get('password1')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')
        print(request.POST)
        try:
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
            )
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        except:
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
                return redirect('dashboard')
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



