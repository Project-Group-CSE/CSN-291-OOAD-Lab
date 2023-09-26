from django.contrib import admin
from users.models import user, credential
# Register your models here.

admin.site.register(user)
admin.site.register(credential)