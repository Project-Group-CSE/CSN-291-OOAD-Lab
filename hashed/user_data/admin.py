from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_data.models import myUser, credential

admin.site.register(myUser, UserAdmin)
admin.site.register(credential)
