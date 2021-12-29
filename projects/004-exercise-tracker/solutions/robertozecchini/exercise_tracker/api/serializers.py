# serializers.py

from rest_framework import serializers

from .models import User, Exercise

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', '_id')

class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercise
        fields = ('description', 'duration', 'date')