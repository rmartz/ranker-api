from django.test import TestCase
from categorizer.models import Topic, Option, TopicOption, Contest
from django.contrib.auth.models import User


# Create your tests here.
class ContestTestCase(TestCase):
    def setUp(self):
        blue = Option.objects.create(label='Blue')
        red = Option.objects.create(label='Red')

        self.topic = Topic.objects.create(label='Favorite color')

        self.blue = TopicOption.objects.create(topic=self.topic, option=blue)
        self.red = TopicOption.objects.create(topic=self.topic, option=red)

        self.user = User.objects.create_user('user', 'user@example.com',
                                             'password')

    def test_create_contest(self):
        contest = Contest.create_random(self.topic, self.user)

        # Ensure that there are two contestants and they are not the same
        self.assertEqual(contest.contestants.distinct().count(), 2)

        self.assertIn(self.red.id, (contest.contestants.all().values_list(
                                 'topicoption__id', flat=True)))
        self.assertIn(self.blue.id, (contest.contestants.all().values_list(
                                  'topicoption__id', flat=True)))

        for contestant in contest.contestants.all():
            self.assertIn(contestant.topicoption, [self.red, self.blue])
            self.assertEqual(contestant.user, self.user)

        # Mark red as the winner
        winner = contest.contestants.get(topicoption=self.red)
        contest.set_winner(winner)

        self.assertEqual(self.red.rankings.get(contest=contest).score, 1008)
        self.assertEqual(self.blue.rankings.get(contest=contest).score, 992)

        top_options = list(self.topic.calculate_top_options(2))
        self.assertEqual(top_options, [self.red, self.blue])
