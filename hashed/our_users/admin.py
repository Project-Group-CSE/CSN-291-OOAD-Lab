from django.contrib import admin
from our_users.models import user, credential

admin.site.register(user)
admin.site.register(credential)