from django import forms
from .models import User

class DriverRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"}),
        label="Пароль"
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}),
        label="Подтвердите пароль"
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "ФИО"}),
        label="ФИО",
        required = True
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "example@gmail.com"}),
        label="Почта",
        required = True
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control","id":"phone_number", "placeholder": "+7 (___) ___-__-__"}),
        label="Телефон",
        required = True
    )
    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "ФИО"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@gmail.com"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 (___) ___-__-__"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data


class OwnerRegistrationForm(DriverRegistrationForm):
    uploaded_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Загрузить файл",
        required=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "uploaded_file", "password"]






