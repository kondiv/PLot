from django import forms
from .models import Parking

class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = ["address", "numbers_of_floors"]
        widgets = {
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите адрес"}),
            "numbers_of_floors": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }
        labels = {
            "address": "Адрес парковки",
            "numbers_of_floors": "Количество этажей",
        }
