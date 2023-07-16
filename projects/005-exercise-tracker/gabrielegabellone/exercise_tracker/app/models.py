from django.db import models
from django.utils import timezone


class User(models.Model):
    """Represents the model of a User in the db.

    :param _id: primary key, a unique alphanumeric string that identifies the user
    :param username: the name of the user
    """
    class Meta:
        db_table = 'users'
    _id = models.CharField(primary_key=True, max_length=24)
    username = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Exercise(models.Model):
    """Represents the model of an Exercise in the db.

    :param user: foreign key, the User object with which the exercise is associated
    :param description: the description of the exercise
    :param duration: the duration of the exercise expressed in minutes
    :param date: the date on which the exercise was performed
    """
    class Meta:
        db_table = 'exercises'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    duration = models.IntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Description: {self.description} Duration: {self.duration} Date: {self.date}"
