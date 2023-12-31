from django.db import models
from django.contrib.auth.models import AbstractUser


class myUser(AbstractUser):
    # database model for users
    email = models.EmailField(blank=False, unique=True)
    hashed_pin = models.CharField(max_length=200, blank=False)
    session_token = models.CharField(max_length=50, blank=True)


class credential(models.Model):
    # database model for credentials associated with users
    website_username = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=False)
    hash_pwd = models.CharField(max_length=200, blank=False)
    strength = models.CharField(max_length=50, blank=False, default="")

    def __str__(self):
        return self.title
