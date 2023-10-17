from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
import uuid


class user(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, blank=False, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=False, unique=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    hashed_password = models.CharField(max_length=200, blank=False)
    hashed_pin = models.CharField(max_length=200, blank=False, editable=False)

    def __str__(self):
        return self.username


class credential(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=False)
    hash_pwd = models.CharField(max_length=200,blank=False)
    strength = models.IntegerField(blank=False)

    def __str__(self):
        return self.title
