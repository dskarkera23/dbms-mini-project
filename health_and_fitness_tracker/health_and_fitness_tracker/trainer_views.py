from django.shortcuts import render, redirect
from app.models import BMILog


def HOME(request):
    return render(request, 'Trainer/home.html')


from django.shortcuts import render
from app.models import BMILog


def trainer_dashboard(request):
    clients_with_bmi = []

    # Loop through each client of the trainer
    for client in request.user.clients.all():
        # Retrieve the latest BMI log for the client
        latest_bmi_log = BMILog.objects.filter(user=client).order_by('-log_date').first()

        # Check if BMI log is available
        if latest_bmi_log:
            latest_bmi = latest_bmi_log.bmi
            bmi_condition = get_bmi_condition(latest_bmi)  # You need to define this function

            # Add client and BMI info to the list
            clients_with_bmi.append({
                'client': client,
                'client_name': client.get_full_name(),
                'latest_bmi': latest_bmi,
                'bmi_condition': bmi_condition,
            })
        else:
            # If no BMI log available, set values to None
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
