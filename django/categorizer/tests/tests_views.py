from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from categorizer.models import Topic, Option, TopicOption


class RestApiTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('user', 'user@example.com',
                                        'password')
        token = Token.objects.create(user=user).key

        self.c = Client(HTTP_AUTHORIZATION='Token %s' % token)

    def test_topic_lifecycle(self):
        response = self.c.get('/api/topics/')
        self.assertEqual(response.json(), [])

        response = self.c.post('/api/topics/', {'label': 'Testing 123'})
        self.assertEqual(response.json(), {'id': 1, 'status': 'created'})

        response = self.c.get('/api/topics/')
        self.assertEqual(response.json(), [{'id': 1, 'label': 'Testing 123'}])

        response = self.c.get('/api/topics/1/')
        self.assertEqual(response.json(), {'id': 1, 'label': 'Testing 123'})

        response = self.c.get('/api/topics/2/')
        self.assertEqual(response.status_code, 404)

        response = self.c.post('/api/topics/1/', {'label': 'Testing 456'})
        self.assertEqual(response.json(), {'id': 1, 'status': 'updated'})

        response = self.c.get('/api/topics/1/')
        self.assertEqual(response.json(), {'id': 1, 'label': 'Testing 456'})

        response = self.c.delete('/api/topics/1/')
        self.assertEqual(response.json(), {'status': 'deleted'})

        response = self.c.get('/api/topics/')
        self.assertEqual(response.json(), [])

        response = self.c.get('/api/topics/1/')
        self.assertEqual(response.status_code, 404)

    def test_option_lifecycle(self):
        response = self.c.get('/api/options/')
        self.assertEqual(response.json(), [])

        response = self.c.post('/api/options/', {'label': 'Testing 123'})
        self.assertEqual(response.json(), {'id': 1, 'status': 'created'})

        response = self.c.get('/api/options/')
        self.assertEqual(response.json(), [{'id': 1, 'label': 'Testing 123'}])

        response = self.c.get('/api/options/1/')
        self.assertEqual(response.json(), {'id': 1, 'label': 'Testing 123'})

        response = self.c.get('/api/options/2/')
        self.assertEqual(response.status_code, 404)

        response = self.c.post('/api/options/1/', {'label': 'Testing 456'})
        self.assertEqual(response.json(), {'id': 1, 'status': 'updated'})

        response = self.c.get('/api/options/1/')
        self.assertEqual(response.json(), {'id': 1, 'label': 'Testing 456'})

        response = self.c.delete('/api/options/1/')
        self.assertEqual(response.json(), {'status': 'deleted'})

        response = self.c.get('/api/options/')
        self.assertEqual(response.json(), [])

        response = self.c.get('/api/options/1/')
        self.assertEqual(response.status_code, 404)

    def test_topic_option_mapping_lifecycle(self):
        topic = Topic.objects.create(label="Test Topic")
        option = Option.objects.create(label="Test Option")

        response = self.c.get('/api/topics/%d/options/' % topic.id)
        self.assertEqual(response.json(), [])

        response = self.c.get('/api/topics/%d/options/%d' % (topic.id,
                                                             option.id))
        self.assertEqual(response.status_code, 404)

        response = self.c.put('/api/topics/%d/options/%d' % (topic.id,
                                                             option.id))
        self.assertEqual(response.json(), {'status': 'created'})

        response = self.c.get('/api/topics/%d/options/%d' % (topic.id,
                                                             option.id))
        self.assertEqual(response.json(), {'status': 'OK'})

        response = self.c.delete('/api/topics/%d/options/%d' % (topic.id,
                                                                option.id))
        self.assertEqual(response.json(), {'status': 'deleted'})

        response = self.c.get('/api/topics/%d/options/' % topic.id)
        self.assertEqual(response.json(), [])

        response = self.c.get('/api/topics/%d/options/%d' % (topic.id,
                                                             option.id))
        self.assertEqual(response.status_code, 404)

    def test_topic_contests(self):
        topic = Topic.objects.create(label="Test Topic")
        first = Option.objects.create(label="Test Option 1")
        second = Option.objects.create(label="Test Option 2")

        TopicOption.objects.create(topic=topic, option=first)

        # Can't view a contest when only one option is configured
        response = self.c.get('/api/topics/%d/contests/' % topic.id)
        self.assertEqual(response.status_code, 400)

        TopicOption.objects.create(topic=topic, option=second)

        response = self.c.get('/api/topics/%d/contests/' % topic.id)
        self.assertEqual(set(response.json()['contestants']),
                         set([first.id, second.id]))

        response = self.c.post('/api/topics/%d/contests/' % topic.id,
                               {'winner': -1})
        self.assertEqual(response.status_code, 400)

        response = self.c.post('/api/topics/%d/contests/' % topic.id,
                               {'winner': first.id})
        self.assertEqual(response.json(), {'status': 'OK'})

        response = self.c.get('/api/topics/%d/rankings/' % topic.id)
        self.assertEqual(response.json(), [
            {'id': first.id, 'label': first.label},
            {'id': second.id, 'label': second.label}
        ])
