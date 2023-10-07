from django.contrib import admin
from user_data.models import myUser, credential

admin.site.register(myUser)
admin.site.register(credential)