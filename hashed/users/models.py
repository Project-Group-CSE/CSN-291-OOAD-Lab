from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid

class user(models.Model):
    #usertoken
    username = models.CharField(max_length=50, default="")
    f_name = models.CharField(max_length=50, default="")
    l_name = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=30, default="")
    #hashed pass
    def __str__(self):
        return self.username
    
class credential(models.Model):
    #usertoken
    title = models.CharField(max_length=50, default="")
    website = models.URLField(max_length=100)
    #hashed pass
    #strength
    def __str__(self):
        return self.title

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email","first_name","last_name"]

    def __str__(self):
        return self.email