from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ExerciseSerializer
from .models import User, Exercise
import json
from django.views.decorators.csrf import csrf_exempt


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

@csrf_exempt 
def CreateExercise(request, _id):
    print("I'm here")
    if request.method == 'GET':
        return Response("GET not implemented", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        try:
            u = User.objects.get(pk = _id)
            print(request.body)
            data = json.loads(request.body)         #why data is not working???
            exercise = Exercise(user = u, description = data['description'], date = data['date'], duration = data['duration'])
            exercise.save(force_insert = True)
            return JsonResponse({'description': exercise.description, 'duration': exercise.duration, 'date': exercise.date})
        except:
            return Response("exercise creation fails", status=status.HTTP_400_BAD_REQUEST)