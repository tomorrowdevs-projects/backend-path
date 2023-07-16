import datetime

from rest_framework import serializers

from app.models import User, Exercise


class UserSerializer(serializers.ModelSerializer):
    """Serializer method that allows saving in the database of the User model."""
    class Meta:
        model = User
        fields = ['_id', 'username']


class ExerciseCreateSerializer(serializers.ModelSerializer):
    """Serializer method that allows saving in the database of the Exercise model."""
    class Meta:
        model = Exercise
        fields = ['description', 'duration', 'date', 'user']


class ExerciseSerializerResponse(serializers.Serializer):
    """Serializer method that allows you to serialize an object of type Exercise to be returned as JSON in the
    response."""
    description = serializers.CharField(max_length=200)
    duration = serializers.IntegerField()
    date = serializers.DateField(format="%a %b %d %Y", default=datetime.datetime.now().date())
