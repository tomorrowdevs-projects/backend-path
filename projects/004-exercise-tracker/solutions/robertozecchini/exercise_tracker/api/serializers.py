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

class LogSerializer(serializers.ModelSerializer):
    log = ExerciseSerializer(many = True, read_only=True)
    count = serializers.SerializerMethodField(read_only=True)
    def get_count(self, user):
        return user.log.count()
    class Meta:
        model = User
        fields = ('username', '_id', 'count', 'log')