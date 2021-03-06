from django.test import TestCase
from categorizer.models import Topic, Option, TopicOption, Contest
from django.contrib.auth.models import User


# Create your tests here.
class ContestTestCase(TestCase):
    def setUp(self):
        self.blue = Option.objects.create(label='Blue', id=1)
        self.red = Option.objects.create(label='Red', id=2)

        self.topic = Topic.objects.create(label='Favorite color', id=3)

        self.blue_map = TopicOption.objects.create(topic=self.topic,
                                                   option=self.blue, id=4)
        self.red_map = TopicOption.objects.create(topic=self.topic,
                                                  option=self.red, id=5)

        self.user = User.objects.create_user('user', 'user@example.com',
                                             'password', id=6)

    def test_create_contest(self):
        contest = Contest.create_random(self.topic, self.user)

        # Ensure that there are two contestants and they are not the same
        self.assertEqual(contest.contestants.distinct().count(), 2)

        self.assertIn(self.red_map.id, (contest.contestants.all().values_list(
                                 'topicoption__id', flat=True)))
        self.assertIn(self.blue_map.id, (contest.contestants.all().values_list(
                                  'topicoption__id', flat=True)))

        for contestant in contest.contestants.all():
            self.assertIn(contestant.topicoption, [self.red_map,
                                                   self.blue_map])
            self.assertEqual(contestant.user, self.user)

        # Mark red as the winner
        winner = contest.contestants.get(topicoption=self.red_map)
        contest.set_winner(winner)

        # Check that we can get a ranking list with a tie
        top_options = list(self.topic.calculate_top_options(2))
        # Either order is OK, since the items have the same score
        self.assertItemsEqual(top_options, [self.red, self.blue])

        self.assertEqual(self.red_map.rankings
                         .get(contest=contest).score, 1008)
        self.assertEqual(self.blue_map.rankings
                         .get(contest=contest).score, 992)

        # Check if marking a second winner causes an error
        second_place = contest.contestants.get(topicoption=self.blue_map)
        self.assertRaises(AssertionError, contest.set_winner, second_place)

        # Check that red is ranked above blue
        top_options = list(self.topic.calculate_top_options(2))
        self.assertEqual(top_options, [self.red, self.blue])
