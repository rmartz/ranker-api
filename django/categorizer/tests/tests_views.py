from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from categorizer.models import (Topic, Option, TopicOption, Contest,
                                OptionRanking)


class TopicApiTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('user', 'user@example.com',
                                        'password')
        token = Token.objects.create(user=user).key

        self.c = Client(HTTP_AUTHORIZATION='Token %s' % token)

    def test_topic_list_empty(self):
        response = self.c.get('/api/topics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_topic_list_noauth(self):
        response = Client().get('/api/topics/')
        self.assertEqual(response.status_code, 401)

    def test_topic_create(self):
        response = self.c.post('/api/topics/', {'label': 'Testing 123'})
        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        topic_id = response_json['id']
        self.assertEqual(response_json, {'id': topic_id, 'status': 'created'})

        topic = Topic.objects.get(id=topic_id)
        self.assertEqual(topic.label, 'Testing 123')

    def test_topic_list(self):
        topic = Topic.objects.create(label='Testing 123')
        response = self.c.get('/api/topics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': topic.id,
                                            'label': topic.label}])

    def test_topic_detail(self):
        topic = Topic.objects.create(label='Testing 123')
        response = self.c.get('/api/topics/%d/' % topic.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': topic.id,
                                           'label': topic.label})

    def test_topic_detail_noauth(self):
        response = Client().get('/api/topics/1/')
        self.assertEqual(response.status_code, 401)

    def test_topic_detail_missing(self):
        response = self.c.get('/api/topics/1/')
        self.assertEqual(response.status_code, 404)

    def test_topic_contests_missing(self):
        response = self.c.get('/api/topics/1/contests')
        self.assertEqual(response.status_code, 404)

    def test_topic_options_list_missing(self):
        response = self.c.get('/api/topics/1/options')
        self.assertEqual(response.status_code, 404)

    def test_topic_options_detail_missing_topic(self):
        response = self.c.get('/api/topics/1/options/1')
        self.assertEqual(response.status_code, 404)

    def test_topic_options_delete_missing_topic(self):
        response = self.c.delete('/api/topics/1/options/1')
        self.assertEqual(response.status_code, 404)

    def test_topic_options_add_missing_topic(self):
        response = self.c.put('/api/topics/1/options/1')
        self.assertEqual(response.status_code, 404)

    def test_topic_options_detail_missing_option(self):
        topic = Topic.objects.create(label='Testing 123')
        response = self.c.get('/api/topics/%d/options/1' % topic.id)
        self.assertEqual(response.status_code, 404)

    def test_topic_options_delete_missing_option(self):
        topic = Topic.objects.create(label='Testing 123')
        response = self.c.delete('/api/topics/%d/options/1' % topic.id)
        self.assertEqual(response.status_code, 404)

    def test_topic_options_add_missing_option(self):
        topic = Topic.objects.create(label='Testing 123')
        response = self.c.put('/api/topics/%d/options/1' % topic.id)
        self.assertEqual(response.status_code, 404)

    def test_topic_update(self):
        topic = Topic.objects.create(label='Testing 123')
        response = self.c.post('/api/topics/%d/' % topic.id,
                               {'label': 'Testing 456'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': topic.id,
                                           'status': 'updated'})

        newTopic = Topic.objects.get(id=topic.id)
        self.assertEqual(newTopic.label, 'Testing 456')

    def test_topic_update_missing(self):
        response = self.c.post('/api/topics/123/', {'label': 'Testing 456'})
        self.assertEqual(response.status_code, 404)

    def test_topic_delete(self):
        topic = Topic.objects.create(label='Testing 123')
        response = self.c.delete('/api/topics/%d/' % topic.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'deleted'})

        with self.assertRaises(Topic.DoesNotExist):
            topic = Topic.objects.get(id=topic.id)

    def test_topic_delete_missing(self):
        response = self.c.delete('/api/topics/1/')
        self.assertEqual(response.status_code, 404)


class OptionApiTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('user', 'user@example.com',
                                        'password')
        token = Token.objects.create(user=user).key

        self.c = Client(HTTP_AUTHORIZATION='Token %s' % token)

    def test_option_list_empty(self):
        response = self.c.get('/api/options/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_option_list_noauth(self):
        response = Client().get('/api/options/')
        self.assertEqual(response.status_code, 401)

    def test_option_create(self):
        response = self.c.post('/api/options/', {'label': 'Testing 123'})
        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        option_id = response_json['id']
        self.assertEqual(response_json, {'id': option_id,
                                         'status': 'created'})

        option = Option.objects.get(id=option_id)
        self.assertEqual(option.label, 'Testing 123')

    def test_option_list(self):
        option = Option.objects.create(label='Testing 123')
        response = self.c.get('/api/options/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': option.id,
                                            'label': 'Testing 123'}])

    def test_option_detail(self):
        option = Option.objects.create(label='Testing 123')
        response = self.c.get('/api/options/%d/' % option.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': option.id,
                                           'label': 'Testing 123'})

    def test_option_detail_missing(self):
        response = self.c.get('/api/options/1/')
        self.assertEqual(response.status_code, 404)

    def test_option_detail_noauth(self):
        response = Client().get('/api/options/1/')
        self.assertEqual(response.status_code, 401)

    def test_option_update(self):
        option = Option.objects.create(label='Testing 123')
        response = self.c.post('/api/options/%d/' % option.id,
                               {'label': 'Testing 456'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': option.id,
                                           'status': 'updated'})

        newOption = Option.objects.get(id=option.id)
        self.assertEqual(newOption.label, 'Testing 456')

    def test_option_update_missing(self):
        response = self.c.post('/api/options/1/', {'label': 'Testing 456'})
        self.assertEqual(response.status_code, 404)

    def test_option_delete(self):
        option = Option.objects.create(label='Testing 123')
        response = self.c.delete('/api/options/%d/' % option.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'deleted'})

        with self.assertRaises(Option.DoesNotExist):
            option = Option.objects.get(id=option.id)

    def test_option_delete_missing(self):
        response = self.c.delete('/api/options/1/')
        self.assertEqual(response.status_code, 404)


class TopicOptionMapTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('user', 'user@example.com',
                                        'password')
        token = Token.objects.create(user=user).key

        self.c = Client(HTTP_AUTHORIZATION='Token %s' % token)

        self.topic = Topic.objects.create(label="Test Topic")
        self.option = Option.objects.create(label="Test Option")

    def test_topic_option_list(self):
        TopicOption.objects.create(topic=self.topic, option=self.option)
        response = self.c.get('/api/topics/%d/options/' % self.topic.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': self.option.id,
                                            'label': self.option.label}])

    def test_topic_option_list_empty(self):
        response = self.c.get('/api/topics/%d/options/' % self.topic.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_topic_option_list_noauth(self):
        response = Client().get('/api/topics/%d/options/' % self.topic.id)
        self.assertEqual(response.status_code, 401)

    def test_topic_option_map_missing(self):
        response = self.c.get('/api/topics/%d/options/1' % self.topic.id)
        self.assertEqual(response.status_code, 404)

    def test_topic_option_map_noauth(self):
        response = Client().get('/api/topics/%d/options/1' % self.topic.id)
        self.assertEqual(response.status_code, 401)

    def test_topic_option_map_create(self):
        response = self.c.put('/api/topics/%d/options/%d' % (self.topic.id,
                                                             self.option.id))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'status': 'created'})
        self.assertTrue(TopicOption.objects.filter(
            topic=self.topic, option=self.option).exists())

    def test_topic_option_map_check(self):
        TopicOption.objects.create(topic=self.topic, option=self.option)
        response = self.c.get('/api/topics/%d/options/%d' % (self.topic.id,
                                                             self.option.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'OK'})

    def test_topic_option_map_delete(self):
        TopicOption.objects.create(topic=self.topic, option=self.option)
        response = self.c.delete('/api/topics/%d/options/%d' %
                                 (self.topic.id, self.option.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'deleted'})

        self.assertFalse(TopicOption.objects.filter(
            topic=self.topic, option=self.option).exists())


class TopicContestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com',
                                             'password')
        token = Token.objects.create(user=self.user).key

        self.c = Client(HTTP_AUTHORIZATION='Token %s' % token)

        self.topic = Topic.objects.create(label="Test Topic")
        self.first = Option.objects.create(label="Test Option 1")
        self.second = Option.objects.create(label="Test Option 2")

        for option in [self.first, self.second]:
            topicoption = TopicOption.objects.create(topic=self.topic,
                                                     option=option)

            OptionRanking.objects.create(topicoption=topicoption,
                                         user=self.user)

        self.contest = Contest.objects.create(user=self.user, topic=self.topic)
        self.contest.contestants = OptionRanking.objects.filter(
                                     topicoption__topic=self.topic,
                                     user=self.user).order_by('id')
        self.contest.save()

    def test_contest_create_fail_no_options(self):
        Contest.objects.all().delete()
        TopicOption.objects.all().delete()
        # Can't view a contest when only one option is configured
        response = self.c.get('/api/topics/%d/contests/' % self.topic.id)
        self.assertEqual(response.status_code, 400)

    def test_contest_get(self):
        response = self.c.get('/api/topics/%d/contests/' % self.topic.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': self.first.id, 'label': self.first.label},
            {'id': self.second.id, 'label': self.second.label}
        ])

    def test_contest_get_deleted_option(self):
        # Ensure that a new contest is generated if a option in the current one
        # is deleted
        # Behind the scenes the current contest should be deleted if any of its
        # options are.
        self.first.delete()
        third = Option.objects.create(label="Test Option 3")
        TopicOption.objects.create(topic=self.topic, option=third)

        response = self.c.get('/api/topics/%d/contests/' % self.topic.id)
        self.assertEqual(response.status_code, 200)
        # Use assertItemsEqual because the order is randomized
        self.assertEqual(response.json(), [
            {'id': self.second.id, 'label': self.second.label},
            {'id': third.id, 'label': third.label}
        ])

    def test_contest_missing(self):
        Topic.objects.all().delete()
        response = self.c.get('/api/topics/1/contests/')
        self.assertEqual(response.status_code, 404)

    def test_contest_get_noauth(self):
        response = Client().get('/api/topics/%d/contests/' % self.topic.id)
        self.assertEqual(response.status_code, 401)

    def test_contest_automatic_create(self):
        Contest.objects.all().delete()
        OptionRanking.objects.all().delete()

        response = self.c.get('/api/topics/%d/contests/' % self.topic.id)
        self.assertEqual(response.status_code, 200)
        # assertItemsEqual because the order is randomized
        self.assertItemsEqual(response.json(), [
            {'id': self.first.id, 'label': self.first.label},
            {'id': self.second.id, 'label': self.second.label}
        ])

    def test_contest_invalid_vote(self):
        response = self.c.post('/api/topics/%d/contests/' % self.topic.id,
                               {'winner': -1})
        self.assertEqual(response.status_code, 400)

    def test_contest_vote(self):
        response = self.c.post('/api/topics/%d/contests/' % self.topic.id,
                               {'winner': self.first.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'OK'})

        self.assertEqual(self.first.topicoption.get(topic=self.topic)
                         .rankings.get(user=self.user).score, 1008)
        self.assertEqual(self.second.topicoption.get(topic=self.topic)
                         .rankings.get(user=self.user).score, 992)

    def test_topic_rankings(self):
        ranking = self.contest.contestants.get(topicoption__option=self.second)
        ranking.score = 1600
        ranking.save()

        response = self.c.get('/api/topics/%d/rankings/' % self.topic.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': self.second.id, 'label': self.second.label},
            {'id': self.first.id, 'label': self.first.label}
        ])

    def test_topic_rankings_noauth(self):
        response = Client().get('/api/topics/%d/rankings/' % self.topic.id)
        self.assertEqual(response.status_code, 401)

    def test_topic_rankings_missing(self):
        Topic.objects.all().delete()
        response = self.c.get('/api/topics/1/rankings/')
        self.assertEqual(response.status_code, 404)
