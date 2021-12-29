from django.db import models

class User(models.Model):
    username = models.CharField(max_length=128)
    _id = models.CharField(max_length=128)

class Exercise(models.Model):
    description = models.CharField(max_length=256)
    duration = models.IntegerField()
    date = models.CharField(max_length=64)