import random
import string
import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.serializers import UserSerializer, ExerciseCreateSerializer, ExerciseSerializerResponse
from app.models import User, Exercise


class UserListCreateAPIView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        id_user = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(24))
        request.data['_id'] = id_user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExerciseCreateAPIView(APIView):

    def post(self, request, _id):
        try:
            user = User.objects.get(pk=_id)
            if user:
                exercise_to_create = request.data
                exercise_to_create['user'] = _id

                # saving the exercise in the db
                if 'date' in request.data:
                    date_string = request.data['date']
                    date = datetime.datetime.strptime(date_string, '%a %b %d %Y').date()
                    exercise_to_create['date'] = date
                serializer = ExerciseCreateSerializer(data=exercise_to_create)
                if serializer.is_valid():
                    serializer.save()

                # serialization of the User object and the Exercise object for the response
                serialized_user = UserSerializer(user).data
                serialized_exercise = ExerciseSerializerResponse(data=request.data)
                if serialized_exercise.is_valid():
                    serialized_exercise = serialized_exercise.data

                data_to_return = serialized_user | serialized_exercise
                return Response(data_to_return, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)


class LogListAPIView(APIView):
    def get(self, request, _id):
        try:
            user = User.objects.get(pk=_id)
            if user:
                exercises = Exercise.objects.filter(user=user)
                log = []

                for e in exercises:
                    field = {'description': e.description, 'duration': e.duration, 'date': e.date}
                    ser = ExerciseSerializerResponse(data=field)
                    if ser.is_valid():
                        log.append(ser.data)

                serialized_user = UserSerializer(user).data
                count = len(exercises)
                serialized_user['count'], serialized_user['log'] = count, log
                return Response(serialized_user, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)