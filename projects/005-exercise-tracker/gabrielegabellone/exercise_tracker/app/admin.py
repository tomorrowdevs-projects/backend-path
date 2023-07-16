from django.contrib import admin

from .models import User, Exercise

admin.site.register(User)
admin.site.register(Exercise)