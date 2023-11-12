from django import forms
from .models import FoodLog  # Import the FoodLog model

class FoodLogForm(forms.ModelForm):
    class Meta:
        model = FoodLog  # Use the FoodLog model
        fields = ['log_date', 'amount_g', 'food']  # Include the desired fields
