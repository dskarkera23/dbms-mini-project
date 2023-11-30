from django import forms
from .models import FoodLog, ExerciseLog, BMILog


class ExerciseLogForm(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ['exercise', 'reps', 'sets', 'log_date']


class FoodLogForm(forms.ModelForm):
    class Meta:
        model = FoodLog
        fields = ['food', 'category', 'log_date', 'amount_g']

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