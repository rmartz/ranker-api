from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class TopicApiTestCase(APITestCase):
    def test_register_success(self):
        response = self.client.post(
            '/auth/user/',
            {'username': 'test',
             'email': 'test@example.com',
             'password': 'password'})

        self.assertEqual(response.status_code, 201)

        response_json = response.json()

        user_class = get_user_model()
        user = user_class.objects.get()
        self.assertEqual(response_json, {'token': user.auth_token.key})
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'test')


class TokenApiTestCase(APITestCase):
    def setUp(self):
        user_class = get_user_model()

        self.user = user_class.objects.create_user('user', 'user@example.com',
                                                   'password')
        self.token = Token.objects.create(user=self.user)

    def test_get_token(self):
        response = self.client.post('/auth/user/token',
                                    {'username': 'user',
                                     'password': 'password'})
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['token'], self.token.key)

    def test_token_reset(self):
        response = self.client.delete('/auth/user/token',
                                      {'username': 'user',
                                       'password': 'password'})
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertNotEqual(response_json['token'], self.token.key)

        new_token = Token.objects.get(user=self.user)
        self.assertNotEqual(response_json['token'], new_token)
