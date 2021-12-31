from django.contrib import admin
from .models import User, Exercise

class ExerciseInline(admin.StackedInline):
    model = Exercise

class UserAdmin(admin.ModelAdmin):
    inlines = [
        ExerciseInline,
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Exercise)