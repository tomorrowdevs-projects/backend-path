from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status

from api.serializers import UserSerializer, ExerciseSerializer
from .models import User, Exercise
from datetime import datetime

client = Client()

class ExerciseTrackerTest(TestCase):
    def setUp(self):
        self.valid_user = {
            'username': 'Mandrake',
        }
        self.valid_exercise = {
            'description': 'Easy exercise for test purpose',
            'duration': 30
        }
        self.test_user = User.objects.create(username='Pinco Pallino')
        self.today = datetime.now().strftime('%a %b %d %Y')
        self.exercise0 = Exercise.objects.create(user = self.test_user, description = 'test0', duration = 5, date = '01/01/1990')
        self.exercise1 = Exercise.objects.create(user = self.test_user, description = 'test1', duration = 5, date = '01/01/1991')
        self.exercise2 = Exercise.objects.create(user = self.test_user, description = 'test2', duration = 5, date = '01/01/1992')
        self.exercise3 = Exercise.objects.create(user = self.test_user, description = 'test3', duration = 5, date = '01/01/1993')
        self.exercise4 = Exercise.objects.create(user = self.test_user, description = 'test4', duration = 5, date = '01/01/1994')

    def tearDown(self):
        pass

    def test_create_user(self):
        response = client.post(
            '/api/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(data.get('username', ''), self.valid_user['username'])
        self.assertEqual(len(data.get('_id', '')), 25)
    
    def test_get_users(self):
        response = client.get('/api/users/')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_exercise(self):
        response = client.post(
            f'/api/users/:{self.test_user._id}/exercises/',
            data=json.dumps(self.valid_exercise),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data.get('description', ''), self.valid_exercise['description'])
        self.assertEqual(data.get('duration', ''), self.valid_exercise['duration'])
        self.assertEqual(data.get('date', ''), self.today)
    
    def test_get_logs(self):
        response = client.get(f'/api/users/:{self.test_user._id}/logs/')
        data = json.loads(response.content)
        exercises = self.test_user.log
        serializer = ExerciseSerializer(exercises, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['log'], serializer.data)
        self.assertEqual(data['count'], len(serializer.data))
        self.assertEqual(data['username'], self.test_user.username)
        self.assertEqual(data['_id'], self.test_user._id)
    
    def test_get_logs_filtered(self):
        arguments = {'limit': 2, 'from': '1990-06-06', 'to': '1993-06-06'}
        response = client.get(f'/api/users/:{self.test_user._id}/logs/', arguments)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 2)