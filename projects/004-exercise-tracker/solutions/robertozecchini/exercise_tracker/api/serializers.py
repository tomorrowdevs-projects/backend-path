# serializers.py

from rest_framework import serializers
from rest_framework.fields import empty
from dateutil.parser import parse
from datetime import date, datetime
from .models import User, Exercise
import sys

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
    def __init__(self, instance=None, data=empty, **kwargs):
        self.log_limit = kwargs.pop('limit', [sys.maxsize])
        self.log_limit = int(self.log_limit[0])
        self.log_from = kwargs.pop('from', [date.min.isoformat()])
        self.log_from = parse(self.log_from[0])
        self.log_to = kwargs.pop('to', [date.max.isoformat()])
        self.log_to = parse(self.log_to[0])
        super().__init__(instance, data, **kwargs)
    def get_count(self, user):
        return user.log.count()
    def get_log(self, user):
        logs = user.log.all()
        dates = [ex.date for ex in logs if parse(ex.date) > self.log_from and parse(ex.date) < self.log_to]
        filtered = logs.filter(date__in = dates)
        serializer = ExerciseSerializer(filtered, many=True)
        return serializer.data[:self.log_limit]
    class Meta:
        model = User
        fields = ('username', '_id', 'count', 'log')