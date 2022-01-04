from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ExerciseSerializer, LogSerializer
from .models import User, Exercise
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from rest_framework.decorators import api_view
from dateutil.parser import parse


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

@csrf_exempt 
def CreateExercise(request, _id):
    if request.method == 'GET':
        return Response("GET not implemented", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        try:
            u = User.objects.get(pk = _id)
            data = json.loads(request.body)
            date = data.get('date', '')
            try:
                date = parse(date)
            except ValueError:
                date = datetime.now()
            date = date.strftime('%a %b %d %Y')
            exercise = Exercise(user = u, description = data['description'], date = date, duration = data['duration'])
            exercise.save(force_insert = True)
            return_value = {
                'username': u.username,
                'description': exercise.description,
                'duration': exercise.duration,
                'date': exercise.date,
                '_id': u._id,
            }
            return JsonResponse(return_value)
        except:
            return Response("exercise creation fails", status=status.HTTP_400_BAD_REQUEST)

#@api_view
def ViewLog(request, _id):
    try:
        if request.method == 'GET':
            u = User.objects.get(pk = _id)
            serializer = LogSerializer(u, **request.GET)
            return JsonResponse(serializer.data)
    except:
        return Response("wrong log request", status=status.HTTP_400_BAD_REQUEST)
