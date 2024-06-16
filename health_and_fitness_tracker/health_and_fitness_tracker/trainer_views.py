from django.shortcuts import render, redirect
from app.models import *
from app.forms import *

def HOME(request):
    return render(request, 'Trainer/home.html')


from django.shortcuts import render
from app.models import BMILog


def trainer_dashboard(request):
    clients_with_bmi = []
    for client in request.user.clients.all():
        latest_bmi_log = BMILog.objects.filter(user=client).order_by('-log_date').first()

        if latest_bmi_log:
            latest_bmi = latest_bmi_log.bmi
            bmi_condition = get_bmi_condition(latest_bmi) 

            clients_with_bmi.append({
                'client': client,
                'client_name': client.get_full_name(),
                'latest_bmi': latest_bmi,
                'bmi_condition': bmi_condition,
            })
        else:
            clients_with_bmi.append({
                'client': client,
                'client_name': client.get_full_name(),
                'latest_bmi': None,
                'bmi_condition': None,
            })

    context = {
        'clients_with_bmi': clients_with_bmi,
    }

    return render(request, 'Trainer/home.html', context)


def get_bmi_condition(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 24.9:
        return 'Healthy weight'
    elif 25 <= bmi < 29.9:
        return 'Overweight'
    else:
        return 'Obesity'


from django.db import IntegrityError

from django.db.models import Q
from app.models import Message
from app.forms import MessageForm
from itertools import chain

def trainer_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')

    all_messages = sorted(chain(sent_messages, received_messages), key=lambda msg: msg.timestamp, reverse=True)

    if request.method == 'POST':
        form = TrainerMessageForm(request.POST, trainer=request.user)
        if form.is_valid():
            content = form.cleaned_data['content']
            receiver_user = form.cleaned_data['receiver']

            try:
                Message.create_message(sender=request.user, receiver=receiver_user, content=content)
                return redirect('trainer_messages')
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
    else:
        form = TrainerMessageForm(trainer=request.user)

    context = {
        'all_messages': all_messages,
        'form': form,
    }

    return render(request, 'Trainer/tmsg.html', context)
