from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, ExerciseSerializer
from .models import User, Exercise


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer