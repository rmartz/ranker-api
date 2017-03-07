from django.test import TestCase
from django.test import Client

c = Client()


class RestApiTestCase(TestCase):
    def test_topic_lifecycle(self):
        response = c.get('/api/topics/')
        self.assertEqual(response.json(), [])

        response = c.post('/api/topics/', {'label': 'Testing 123'})
        self.assertEqual(response.json(), {'id': 1, 'status': 'created'})

        response = c.get('/api/topics/')
        self.assertEqual(response.json(), [{'id': 1, 'label': 'Testing 123'}])

        response = c.get('/api/topics/1/')
        self.assertEqual(response.json(), {'id': 1, 'label': 'Testing 123'})

        response = c.get('/api/topics/2/')
        self.assertEqual(response.status_code, 404)

        response = c.post('/api/topics/1/', {'label': 'Testing 456'})
        self.assertEqual(response.json(), {'id': 1, 'status': 'updated'})

        response = c.get('/api/topics/1/')
        self.assertEqual(response.json(), {'id': 1, 'label': 'Testing 456'})

        response = c.delete('/api/topics/1/')
        self.assertEqual(response.json(), {'id': 1, 'status': 'deleted'})

        response = c.get('/api/topics/')
        self.assertEqual(response.json(), [])

        response = c.get('/api/topics/1/')
        self.assertEqual(response.status_code, 404)

    def test_option_lifecycle(self):
        response = c.get('/api/options/')
        self.assertEqual(response.json(), [])

        response = c.post('/api/options/', {'label': 'Testing 123'})
        self.assertEqual(response.json(), {'id': 1, 'status': 'created'})

        response = c.get('/api/options/')
        self.assertEqual(response.json(), [{'id': 1, 'label': 'Testing 123'}])

        response = c.get('/api/options/1/')
        self.assertEqual(response.json(), {'id': 1, 'label': 'Testing 123'})

        response = c.get('/api/options/2/')
        self.assertEqual(response.status_code, 404)

        response = c.post('/api/options/1/', {'label': 'Testing 456'})
        self.assertEqual(response.json(), {'id': 1, 'status': 'updated'})

        response = c.get('/api/options/1/')
        self.assertEqual(response.json(), {'id': 1, 'label': 'Testing 456'})

        response = c.delete('/api/options/1/')
        self.assertEqual(response.json(), {'id': 1, 'status': 'deleted'})

        response = c.get('/api/options/')
        self.assertEqual(response.json(), [])

        response = c.get('/api/options/1/')
        self.assertEqual(response.status_code, 404)
