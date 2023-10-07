from django.contrib import admin
from users.models import user, credential

admin.site.register(user)
admin.site.register(credential)