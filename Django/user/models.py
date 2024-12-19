import datetime
from datetime import datetime
import jwt
import re
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
)

def validate_phone_number(value):
    pattern = r"^\+\d{1,3} \(\d{3}\) \d{3}-\d{4}$"
    if not re.match(pattern, value):
        raise ValidationError(
            "Номер телефона должен быть в формате: +1 (234) 567-4890"
        )

def validate_full_name(value):
    pattern = r'^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            "ФИО должно быть в формате: Фамилия Имя Отчество (с заглавной буквы)"
        )

def user_directory_path(instance, filename):
    return f'uploads/user_{instance.email}/{filename}'

class User(AbstractUser):
    ADMIN = "admin"
    PARKINGOWNER = "parkingowner"
    DRIVER = "driver"

    ROLES = (
        (ADMIN, "Администратор"),
        (PARKINGOWNER, "Владелец"),
        (DRIVER, "Водитель"),
    )

    role = models.CharField(
        max_length=100, verbose_name="Роль", choices=ROLES, default=DRIVER
    )

    username = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name="ФИО пользователя",
    )

    email = models.EmailField(
        max_length=60,
        unique=True,
        blank=False,
        null=False
    )

    phone_number = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        validators=[validate_phone_number],
    )

    uploaded_file = models.FileField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        verbose_name="Загруженный файл"
    )

    confirmation_code = models.CharField(max_length=6, default='000000')

    bio = models.TextField(
        'Биография пользователя',
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_parkingowner(self):
        return self.role == self.PARKINGOWNER

    @property
    def is_diver(self):
        return self.role == self.DRIVER

    @property
    def token(self) -> str:

        return self._generate_jwt_token()

    def _generate_jwt_token(self) -> str:

        dt = datetime.now() + datetime.timedelta(days=1)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token


    def get_first_name(self):
        parts = self.username.split()
        return parts[1] if len(parts) > 1 else parts[0]

    def get_second_name(self):
        parts = self.username.split()
        return parts[0] if len(parts) > 1 else parts[0]

    def get_third_name(self):
        parts = self.username.split()
        return parts[2] if len(parts) > 1 else parts[0]


