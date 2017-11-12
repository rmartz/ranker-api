from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TopicApiTestCase(APITestCase):
    def test_register_success(self):
        user_creds = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password'
        }

        url = reverse('auth_user')
        response = self.client.post(url, user_creds)

        self.assertEqual(response.status_code, 201)

        response_json = response.json()

        user_class = get_user_model()
        user = user_class.objects.get()
        self.assertEqual(response_json, {'token': user.auth_token.key})
        self.assertEqual(user.email, user_creds['email'])
        self.assertEqual(user.username, user_creds['username'])


class TokenApiTestCase(APITestCase):
    def setUp(self):
        user_class = get_user_model()

        self.user_cred = {
            'username': 'user',
            'password': 'password'
        }

        self.user = user_class.objects.create_user(email='user@example.com',
                                                   **self.user_cred)
        self.token = Token.objects.create(user=self.user)

    def test_get_token(self):
        url = reverse('auth_token')
        response = self.client.post(url, self.user_cred)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['token'], self.token.key)

    def test_get_token_failure(self):
        url = reverse('auth_token')
        response = self.client.post(url,
                                    dict(self.user_cred, password='badpass'))
        self.assertEqual(response.status_code, 403)

    def test_token_reset(self):
        url = reverse('auth_token')
        response = self.client.delete(url, self.user_cred)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertNotEqual(response_json['token'], self.token.key)

        new_token = Token.objects.get(user=self.user)
        self.assertNotEqual(response_json['token'], new_token)

    def test_token_failure(self):
        url = reverse('auth_token')
        response = self.client.delete(url,
                                      dict(self.user_cred, password='badpass'))
        self.assertEqual(response.status_code, 403)
