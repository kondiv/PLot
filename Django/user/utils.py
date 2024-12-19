from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import os

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None