from django import forms
from .models import *


class ExerciseLogForm(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ['exercise', 'reps', 'sets', 'log_date']


class FoodLogForm(forms.ModelForm):
    class Meta:
        model = FoodLog
        fields = ['food', 'category', 'log_date', 'qty']

    def __init__(self, *args, **kwargs):
        food_items = kwargs.pop('food_items', None)
        super(FoodLogForm, self).__init__(*args, **kwargs)

        # Populate the 'food' field choices with the provided food_items queryset
        if food_items:
            self.fields['food'].queryset = food_items


class BMILogForm(forms.ModelForm):
    class Meta:
        model = BMILog
        fields = ['height', 'weight', 'log_date']


# forms.py
# app/forms.py

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # Include the receiver field


# app/forms.py

# app/forms.py

# app/forms.py

# app/forms.py

# Update TrainerMessageForm to filter clients for the logged-in trainer
class TrainerMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)
        super(TrainerMessageForm, self).__init__(*args, **kwargs)

        if trainer:
            # Set the trainer as the sender and update the queryset for the receiver field
            self.fields['sender'].initial = trainer
            self.fields['sender'].widget = forms.HiddenInput()
            self.fields['receiver'].queryset = CustomUser.objects.filter(selected_trainer=trainer, user_type='1')

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content']