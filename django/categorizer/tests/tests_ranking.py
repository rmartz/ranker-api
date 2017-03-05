from django.test import TestCase
from categorizer.ranked_preference import instant_runoff, full_ranked_preference


# Create your tests here.
class ContestTestCase(TestCase):
    def test_instant_runoff(self):
        candidates = ['Blue', 'Red', 'Green']
        votes = [
            ['Red', 'Blue', 'Green'],
            ['Blue', 'Red'],
            ['Blue', 'Green', 'Red'],
            ['Green', 'Red'],
            ['Green', 'Blue', 'Red']
        ]

        # Round 1: Red gets only 1 vote, drops out
        # Roud 2: Blue gets 3 votes, wins
        winner = instant_runoff(candidates, votes)
        self.assertEqual(winner, 'Blue')

    def test_full_ranked_preference(self):
        candidates = ['Blue', 'Red', 'Green']
        votes = [
            ['Red', 'Blue', 'Green'],
            ['Blue', 'Red'],
            ['Blue', 'Green', 'Red'],
            ['Green', 'Red'],
            ['Green', 'Blue', 'Red']
        ]

        # Round 1: Red gets only 1 vote, drops out
        # Round 2: Blue gets 3 votes, wins 1st place
        # Repeat without Blue
        # Round 1: Green gets 3 votes, wins 2nd place
        # Repeat without Blue or Green
        # Round 1: Red gets 5 votes, wins 3rd place
        winners = list(full_ranked_preference(candidates, votes))
        self.assertEqual(winners, ['Blue', 'Green', 'Red'])
