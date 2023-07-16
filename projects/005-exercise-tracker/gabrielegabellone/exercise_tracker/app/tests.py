import json
import datetime
from datetime import date

from django.test import TestCase
from rest_framework.test import RequestsClient

from app.models import User, Exercise
from app.api import views

views.random.seed(10)


class AppTestCase(TestCase):
    def setUp(self):
        users = [('5fb5853f734231456ccb3b05', 'fcc_test'), ('PD43bXqpxAwGcXc4k4qd2KHl', 'gabriele')]
        for user in users:
            User.objects.create(_id=user[0], username=user[1])

        self.user = User.objects.get(_id='5fb5853f734231456ccb3b05')
        exercises = [(self.user, 'test', 60, datetime.date(1990, 1, 1)), (self.user, 'test2', 30, datetime.date(1990, 1, 2))]
        for exercise in exercises:
            Exercise.objects.create(user=exercise[0], description=exercise[1], duration=exercise[2], date=exercise[3])

        self.client = RequestsClient()

    def test_models_to_str(self):
        """Tests that the models are correctly represented as strings."""
        user = User.objects.get(_id='5fb5853f734231456ccb3b05')
        exercise = Exercise.objects.get(user=user, description='test')
        self.assertEqual(str(user), 'fcc_test')
        self.assertEqual(str(exercise), 'Description: test Duration: 60 Date: 1990-01-01')

    def test_get_users(self):
        """Tests that the request returns the list of all users."""
        response = self.client.get('http://testserver/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'[{"_id":"5fb5853f734231456ccb3b05","username":"fcc_test"},{"_id":"PD43bXqpxAwGcXc4k4qd2KHl",'
                      b'"username":"gabriele"}]', response.content)

    def test_post_users(self):
        """Tests that the request performs the creation of the user."""
        response = self.client.post('http://testserver/api/users/', json={'username': 'test'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'{"_id":"qjcbeEplU2gK1OaPCCfT0mqE","username":"test"}', response.content)

    def test_post_exercise(self):
        """Tests that the request creates the exercise."""
        id_user = self.user._id
        response = self.client.post(f'http://testserver/api/users/:{id_user}/exercises',
                                    json={'description': 'new exercise', 'duration': 30, 'date': 'Sun Jul 16 2023'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'{"_id":"5fb5853f734231456ccb3b05","username":"fcc_test","description":"new exercise",'
                      b'"duration":30,"date":"Sun Jul 16 2023"}', response.content)

    def test_post_exercise_date_not_provided(self):
        """Tests that the request creates the exercise on the current date if it is not provided."""
        id_user = self.user._id
        response = self.client.post(f'http://testserver/api/users/:{id_user}/exercises',
                                    json={'description': 'new exercise', 'duration': 30})
        self.assertEqual(response.status_code, 201)

        current_date = date.today().strftime('%a %b %d %Y')
        expected_json = {'_id': '5fb5853f734231456ccb3b05', 'username': 'fcc_test', 'description': 'new exercise', 'duration': 30, 'date': f'{current_date}'}
        actual_json = json.loads(response.content)
        self.assertEqual(actual_json, expected_json)

    def test_post_exercise_user_not_found(self):
        """Test the request response when creating an exercise for a user that doesn't exist in the db."""
        id_user = 1
        response = self.client.post(f'http://testserver/api/users/:{id_user}/exercises',
                                    json={'description': 'new exercise', 'duration': 30, 'date': 'Sun Jul 16 2023'})
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'{"error":"user not found"}', response.content)

    def test_get_logs(self):
        """Test the request response when trying to get the log for a user."""
        id_user = self.user._id
        response = self.client.get(f'http://testserver/api/users/:{id_user}/logs')
        self.assertEqual(response.status_code, 200)
        self.assertIn( b'{"_id":"5fb5853f734231456ccb3b05","username":"fcc_test","count":2,"log":[{'
                       b'"description":"test","duration":60,"date":"Mon Jan 01 1990"},{"description":"test2",'
                       b'"duration":30,"date":"Tue Jan 02 1990"}]}', response.content)

    def test_get_logs_user_not_found(self):
        """Test the request response when trying to get the log for a user that doesn't exist in the db."""
        id_user = 1
        response = self.client.get(f'http://testserver/api/users/:{id_user}/logs')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'{"error":"user not found"}', response.content)
