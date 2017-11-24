from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from categorizer.models import (Topic, Option, TopicOption, Contest,
                                OptionRanking)


class TopicApiTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('user', 'user@example.com',
                                        'password')
        Token.objects.create(user=user).key
        self.client.force_authenticate(user=user)

    def test_topic_list_empty(self):
        url = reverse('ranker-topics-list')
        response = self.client.get(url)
        self.assertEqual(response.json(), [])
        self.assertEqual(response.status_code, 200)

    def test_topic_list_noauth(self):
        self.client.logout()
        url = reverse('ranker-topics-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_topic_create(self):
        url = reverse('ranker-topics-list')
        response = self.client.post(url, {'label': 'Testing 123'})
        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        topic = Topic.objects.get()
        self.assertEqual(response_json, {'id': topic.id,
                                         'label': topic.label})
        self.assertEqual(topic.label, 'Testing 123')

    def test_topic_list(self):
        topic = Topic.objects.create(label='Testing 123')
        url = reverse('ranker-topics-list')
        response = self.client.get(url)
        self.assertEqual(response.json(), [{'id': topic.id,
                                            'label': topic.label}])
        self.assertEqual(response.status_code, 200)

    def test_topic_detail(self):
        topic = Topic.objects.create(label='Testing 123')
        url = reverse('ranker-topics-detail', kwargs={'pk': topic.id})
        response = self.client.get(url)
        self.assertEqual(response.json(), {'id': topic.id,
                                           'label': topic.label})
        self.assertEqual(response.status_code, 200)

    def test_topic_detail_noauth(self):
        self.client.logout()
        url = reverse('ranker-topics-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_topic_detail_missing(self):
        url = reverse('ranker-topics-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_contests_missing(self):
        url = reverse('ranker-topics-contest', kwargs={'topic_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_options_list_missing(self):
        url = reverse('ranker-topics-options', kwargs={'topic_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_options_detail_missing_topic(self):
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': 1, 'option_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_options_delete_missing_topic(self):
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': 1, 'option_id': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_options_add_missing_topic(self):
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': 1, 'option_id': 1})
        response = self.client.put(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_options_detail_missing_option(self):
        topic = Topic.objects.create(label='Testing 123')
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': topic.id, 'option_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_options_delete_missing_option(self):
        topic = Topic.objects.create(label='Testing 123')
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': topic.id, 'option_id': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_options_add_missing_option(self):
        topic = Topic.objects.create(label='Testing 123')
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': topic.id, 'option_id': 1})
        response = self.client.put(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_update(self):
        topic = Topic.objects.create(label='Testing 123')
        url = reverse('ranker-topics-detail', kwargs={'pk': topic.id})
        response = self.client.put(url, {'label': 'Testing 456'})

        self.assertEqual(response.json(), {'id': topic.id,
                                           'label': 'Testing 456'})
        newTopic = Topic.objects.get(id=topic.id)
        self.assertEqual(newTopic.label, 'Testing 456')
        self.assertEqual(response.status_code, 200)

    def test_topic_update_missing(self):
        url = reverse('ranker-topics-detail', kwargs={'pk': 123})
        response = self.client.put(url, {'label': 'Testing 456'})
        self.assertEqual(response.status_code, 404)

    def test_topic_delete(self):
        topic = Topic.objects.create(label='Testing 123')
        url = reverse('ranker-topics-detail', kwargs={'pk': topic.id})
        response = self.client.delete(url)

        self.assertFalse(Topic.objects.filter(id=topic.id).exists())
        self.assertEqual(response.status_code, 204)

    def test_topic_delete_missing(self):
        url = reverse('ranker-topics-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)


class OptionApiTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('user', 'user@example.com',
                                        'password')
        Token.objects.create(user=user).key

        self.client.force_authenticate(user=user)

    def test_option_list_empty(self):
        url = reverse('ranker-options-list')
        response = self.client.get(url)
        self.assertEqual(response.json(), [])
        self.assertEqual(response.status_code, 200)

    def test_option_list_noauth(self):
        self.client.logout()
        url = reverse('ranker-options-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_option_create(self):
        url = reverse('ranker-options-list')
        response = self.client.post(url, {'label': 'Testing 123'})

        option = Option.objects.get()
        self.assertEqual(response.json(), {'id': option.id,
                                           'label': option.label})
        self.assertEqual(option.label, 'Testing 123')
        self.assertEqual(response.status_code, 201)

    def test_option_list(self):
        option = Option.objects.create(label='Testing 123')
        url = reverse('ranker-options-list')
        response = self.client.get(url)
        self.assertEqual(response.json(), [{'id': option.id,
                                            'label': 'Testing 123'}])
        self.assertEqual(response.status_code, 200)

    def test_option_detail(self):
        option = Option.objects.create(label='Testing 123')
        url = reverse('ranker-options-detail', kwargs={'pk': option.id})
        response = self.client.get(url)
        self.assertEqual(response.json(), {'id': option.id,
                                           'label': 'Testing 123'})
        self.assertEqual(response.status_code, 200)

    def test_option_detail_missing(self):
        url = reverse('ranker-options-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_option_detail_noauth(self):
        self.client.logout()
        url = reverse('ranker-options-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_option_update(self):
        option = Option.objects.create(label='Testing 123')
        url = reverse('ranker-options-detail', kwargs={'pk': option.id})
        response = self.client.put(url, {'label': 'Testing 456'})
        self.assertEqual(response.json(), {'id': option.id,
                                           'label': 'Testing 456'})

        option.refresh_from_db()
        self.assertEqual(option.label, 'Testing 456')
        self.assertEqual(response.status_code, 200)

    def test_option_update_missing(self):
        url = reverse('ranker-options-detail', kwargs={'pk': 1})
        response = self.client.put(url, {'label': 'Testing 456'})
        self.assertEqual(response.status_code, 404)

    def test_option_delete(self):
        option = Option.objects.create(label='Testing 123')
        url = reverse('ranker-options-detail', kwargs={'pk': option.id})
        response = self.client.delete(url)

        self.assertFalse(Option.objects.filter(id=option.id).exists())
        self.assertEqual(response.status_code, 204)

    def test_option_delete_missing(self):
        url = reverse('ranker-options-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)


class TopicOptionMapTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('user', 'user@example.com',
                                        'password')
        Token.objects.create(user=user).key

        self.client.force_authenticate(user=user)

        self.topic = Topic.objects.create(label="Test Topic")
        self.option = Option.objects.create(label="Test Option")

    def test_topic_option_list(self):
        TopicOption.objects.create(topic=self.topic, option=self.option)
        url = reverse('ranker-topics-options',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.json(), [{'id': self.option.id,
                                            'label': self.option.label}])
        self.assertEqual(response.status_code, 200)

    def test_topic_option_list_empty(self):
        url = reverse('ranker-topics-options',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.json(), [])
        self.assertEqual(response.status_code, 200)

    def test_topic_option_list_noauth(self):
        self.client.logout()
        url = reverse('ranker-topics-options',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_topic_option_map_missing(self):
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': self.topic.id, 'option_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_option_map_noauth(self):
        self.client.logout()
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': self.topic.id, 'option_id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_topic_option_map_create(self):
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': self.topic.id,
                              'option_id': self.option.id})
        response = self.client.put(url)
        self.assertTrue(TopicOption.objects.filter(
            topic=self.topic, option=self.option).exists())
        self.assertEqual(response.status_code, 201)

    def test_topic_option_map_check(self):
        TopicOption.objects.create(topic=self.topic, option=self.option)
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': self.topic.id,
                              'option_id': self.option.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_topic_option_map_delete(self):
        TopicOption.objects.create(topic=self.topic, option=self.option)
        url = reverse('ranker-topics-option-detail',
                      kwargs={'topic_id': self.topic.id,
                              'option_id': self.option.id})
        response = self.client.delete(url)

        self.assertFalse(TopicOption.objects.filter(
            topic=self.topic, option=self.option).exists())
        self.assertEqual(response.status_code, 200)


class TopicContestTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com',
                                             'password')
        Token.objects.create(user=self.user).key

        self.client.force_authenticate(user=self.user)

        self.topic = Topic.objects.create(label="Test Topic", id=4)
        self.first = Option.objects.create(label="Test Option 1", id=5)
        self.second = Option.objects.create(label="Test Option 2", id=6)

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
        url = reverse('ranker-topics-contest',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_contest_get(self):
        url = reverse('ranker-topics-contest',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.json(), [
            {'id': self.first.id, 'label': self.first.label},
            {'id': self.second.id, 'label': self.second.label}
        ])

        # Ensure that no new contests were created
        self.assertEqual(Contest.objects.all().count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_contest_get_deleted_option(self):
        # Ensure that a new contest is generated if a option in the current one
        # is deleted
        # Behind the scenes the current contest should be deleted if any of its
        # options are.
        self.first.delete()
        third = Option.objects.create(label="Test Option 3")
        TopicOption.objects.create(topic=self.topic, option=third)

        url = reverse('ranker-topics-contest',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)

        # Use assertItemsEqual because the order is randomized
        self.assertEqual(response.json(), [
            {'id': self.second.id, 'label': self.second.label},
            {'id': third.id, 'label': third.label}
        ])
        self.assertEqual(response.status_code, 200)

    def test_contest_missing(self):
        Topic.objects.all().delete()
        url = reverse('ranker-topics-contest', kwargs={'topic_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_contest_get_noauth(self):
        self.client.logout()
        url = reverse('ranker-topics-contest',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_contest_automatic_create(self):
        Contest.objects.all().delete()
        OptionRanking.objects.all().delete()

        url = reverse('ranker-topics-contest',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)

        # assertItemsEqual because the order is randomized
        self.assertItemsEqual(response.json(), [
            {'id': self.first.id, 'label': self.first.label},
            {'id': self.second.id, 'label': self.second.label}
        ])
        self.assertEqual(response.status_code, 200)

    def test_contest_invalid_vote(self):
        url = reverse('ranker-topics-contest',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.post(url, {'winner': -1})
        self.assertEqual(response.status_code, 400)

    def test_contest_vote(self):
        url = reverse('ranker-topics-contest',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.post(url, {'winner': self.first.id})
        self.assertEqual(self.first.topicoption.get(topic=self.topic)
                         .rankings.get(user=self.user).score, 1008)
        self.assertEqual(self.second.topicoption.get(topic=self.topic)
                         .rankings.get(user=self.user).score, 992)
        self.assertEqual(response.status_code, 200)

    def test_contest_create_next(self):
        # Ensure that a new contest is created once the previous one has been
        # voted.
        self.contest.set_winner(
            self.contest.contestants.get(topicoption__option=self.second)
        )

        response = self.client.get('/api/topics/%d/contests/' % self.topic.id)
        self.assertEqual(response.status_code, 200)
        # assertItemsEqual because the order is randomized
        self.assertItemsEqual(response.json(), [
            {'id': self.first.id, 'label': self.first.label},
            {'id': self.second.id, 'label': self.second.label}
        ])

        # Ensure that a new contest was created
        self.assertEqual(Contest.objects.all().count(), 2)

    def test_contest_delete(self):
        url = reverse('ranker-topics-contest',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.delete(url)

        # There should not be any contests remaining
        self.assertFalse(Contest.objects.all().exists())
        self.assertEqual(response.status_code, 200)

    def test_topic_rankings(self):
        ranking = self.contest.contestants.get(topicoption__option=self.second)
        ranking.score = 1600
        ranking.save()

        url = reverse('ranker-topics-rankings', kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)

        self.assertEqual(response.json(), [
            {'id': self.second.id, 'label': self.second.label},
            {'id': self.first.id, 'label': self.first.label}
        ])
        self.assertEqual(response.status_code, 200)

    def test_topic_rankings_limit(self):
        ranking = self.contest.contestants.get(topicoption__option=self.second)
        ranking.score = 1600
        ranking.save()

        url = reverse('ranker-topics-rankings',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get('{}?count=1'.format(url))

        self.assertEqual(response.json(), [
            {'id': self.second.id, 'label': self.second.label}
        ])
        self.assertEqual(response.status_code, 200)

    def test_topic_rankings_tie(self):
        url = reverse('ranker-topics-rankings',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)

        # Either order is OK since it's a tie
        self.assertItemsEqual(response.json(), [
            {'id': self.second.id, 'label': self.second.label},
            {'id': self.first.id, 'label': self.first.label}
        ])
        self.assertEqual(response.status_code, 200)

    def test_topic_rankings_noauth(self):
        self.client.logout()
        url = reverse('ranker-topics-rankings',
                      kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_topic_rankings_missing(self):
        Topic.objects.all().delete()
        url = reverse('ranker-topics-rankings', kwargs={'topic_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
