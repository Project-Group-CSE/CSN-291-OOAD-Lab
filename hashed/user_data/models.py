from django.db import models
from django.contrib.auth.models import AbstractUser


class myUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    hashed_pin = models.CharField(max_length=200, blank=False)

    USERNAME_FIELD = 'email'


class credential(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=False)
    hash_pwd = models.CharField(max_length=200, blank=False)
    strength = models.IntegerField(blank=False)

    def __str__(self):
        return self.title
