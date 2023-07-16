import random
import string
import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.api.serializers import UserSerializer, ExerciseCreateSerializer, ExerciseSerializerResponse
from app.models import User, Exercise


class UserListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_description='Endpoint that allows you to see the list of users in the db.',
        responses={
            '200': openapi.Response(
                description='Success',
                examples={
                    'application/json': [
                        {
                            'username': 'fcc_test',
                            '_id': '5fb5853f734231456ccb3b05'
                        },
                        {
                            'username': 'gabriele',
                            '_id': 'PD43bXqpxAwGcXc4k4qd2KHl',
                        }
                    ]
                }
            )
        })
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Endpoint that allows the creation of a new user in the db.',
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='the name of the user to create')}),
        responses={
            '201': openapi.Response(
                description='Success',
                examples={
                    'application/json': {
                        'username': 'fcc_test',
                        '_id': '5fb5853f734231456ccb3b05'
                    }
                }
            ),
            '400': openapi.Response(
                description='Bad Request',
            ),
        })
    def post(self, request):
        id_user = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(24))
        request.data['_id'] = id_user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExerciseCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_description='Endpoint that allows the insertion of an exercise in the db',
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties=
        {
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='a description of the exercise'),
            'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description='the duration expressed in minutes'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, description='a date in the format "Mon Jan 01 1990", '
                                                                         'defaults to the current date if not provided')
        }),
        responses={
            '201': openapi.Response(
                description='Success',
                examples={
                    'application/json': {
                        'username': 'fcc_test',
                        'description': 'test',
                        'duration': 60,
                        'date': 'Mon Jan 01 1990',
                        '_id': '5fb5853f734231456ccb3b05'
                    }
                }
            ),
            '404': openapi.Response(
                description='User not found',
            ),
        })
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
    @swagger_auto_schema(
        operation_description='Endpoint that allows you to view all the exercises performed by a specific user.',
        responses={
            '200': openapi.Response(
                description='Success',
                examples={
                    'application/json':
                        {
                            'username': 'fcc_test',
                            'count': 1,
                            '_id': '5fb5853f734231456ccb3b05',
                            'log': [
                                {
                                    'description': 'test',
                                    'duration': 60,
                                    'date': 'Mon Jan 01 1990'
                                },
                                {
                                    'description': 'test2',
                                    'duration': 30,
                                    'date': 'Tue Jan 02 1990'
                                }
                            ]
                        }
                }
            ),
            '404': openapi.Response(
                description='User not found',
            ),
        })
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
