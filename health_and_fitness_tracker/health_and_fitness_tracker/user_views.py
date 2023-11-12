from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def HOME(request):
    return render(request,'User/home.html')

@login_required(login_url='/')
def FOOD_LOG(request):
    return render(request,'User/food_log.html')

@login_required(login_url='/')
def EXE_LOG(request):
    return render(request,'User/exe_log.html')