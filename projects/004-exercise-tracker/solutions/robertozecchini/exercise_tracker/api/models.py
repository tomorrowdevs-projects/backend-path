import uuid
from django.db import models
from django.utils.http import int_to_base36


ID_LENGTH = 25

def id_gen() -> str:
    """Generates random string whose length is `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:ID_LENGTH]

class User(models.Model):
    username = models.CharField(max_length=128)
    _id = models.CharField(max_length=ID_LENGTH, primary_key=True, default=id_gen, editable=False)

class Exercise(models.Model):
    user = models.ForeignKey(User, related_name='log', on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    duration = models.IntegerField()
    date = models.CharField(max_length=64)