# serializers.py

from rest_framework import serializers
from dateutil.parser import parse

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
    #log = ExerciseSerializer(many = True, read_only=True)
    log = serializers.SerializerMethodField(read_only=True)
    count = serializers.SerializerMethodField(read_only=True)
    def get_count(self, user):
        return user.log.count()
    def get_log(self, user):
        d_from = parse('2021-01-01')
        d_to = parse('2023-01-01')
        limit = 1
        logs = user.log.all()
        dates = [ex.date for ex in logs if parse(ex.date) > d_from and parse(ex.date) < d_to]
        filtered = logs.filter(date__in = dates)
        serializer = ExerciseSerializer(filtered, many=True)
        return serializer.data[:limit]
    class Meta:
        model = User
        fields = ('username', '_id', 'count', 'log')