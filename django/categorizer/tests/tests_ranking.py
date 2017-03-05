from django.test import TestCase
from categorizer.ranked_preference import (instant_runoff,
                                           full_ranked_preference,
                                           condorcet_winner)


# Create your tests here.
class RankedPreferenceTestCase(TestCase):
    def setUp(self):
        self.candidates = ['Blue', 'Red', 'Green', 'Yellow']
        self.simple_election = [
            ['Red', 'Blue'],
            ['Blue'],
            ['Red']
        ]
        self.tied_plurality = [
            ['Red', 'Blue', 'Green'],
            ['Blue', 'Red'],
            ['Blue', 'Green', 'Red'],
            ['Green', 'Red'],
            ['Green', 'Blue', 'Red']
        ]
        self.spoiler_effect = [
            ['Red', 'Yellow', 'Green'],
            ['Yellow', 'Red'],
            ['Yellow', 'Red'],
            ['Green', 'Yellow', 'Red'],
            ['Green', 'Red', 'Yellow'],
            ['Blue'],
            ['Blue'],
            ['Blue'],
            ['Blue'],
        ]
        self.circular_loop = [
            ['Red', 'Blue', 'Green'],
            ['Blue', 'Green', 'Red'],
            ['Green', 'Red', 'Blue']
        ]

    def test_instant_runoff(self):
        # Round 1: Red gets only 1 vote, drops out
        # Round 2: Blue gets 3 votes, wins
        winner = instant_runoff(self.candidates, self.tied_plurality)
        self.assertEqual(winner, 'Blue')

        # Round 1: Red gets only 1 vote, drops out
        # Round 2: Green gets only 2 votes, drops out
        # Round 3: Yellow gets 5 votes, wins
        winner = instant_runoff(self.candidates, self.spoiler_effect)
        self.assertEqual(winner, 'Yellow')

        # In a circular loop, all candidates tie first round
        winner = instant_runoff(self.candidates, self.circular_loop)
        self.assertEqual(set(winner), set(['Red', 'Blue', 'Green']))

    def test_full_ranked_preference(self):
        # Round 1: Red gets only 1 vote, drops out
        # Round 2: Blue gets 3 votes, wins 1st place
        # Repeat without Blue
        # Round 1: Green gets 3 votes, wins 2nd place
        # Repeat without Blue or Green
        # Round 1: Red gets 5 votes, wins 3rd place
        winners = list(full_ranked_preference(self.candidates,
                                              self.tied_plurality))
        self.assertEqual(winners, ['Blue', 'Green', 'Red'])

        # Yellow wins 1st place
        # Repeat without Yellow
        # Round 1: Green gets only 2 votes, dops out
        # Round 2: Red gets 5 votes, wins 2nd place
        # Repeat without Yellow or Red
        # Round 1: Blue gets 4 votes, wins 3rd place
        # Repeat without Yellow, Red or Blue
        # Round 1: Green gets 3 votes, wins 4th place
        winner = list(full_ranked_preference(self.candidates,
                                             self.spoiler_effect))
        self.assertEqual(winner, ['Yellow', 'Red', 'Blue', 'Green'])

    def test_condorcet_winner(self):
        # Red v Green: Green wins with 3 over 2
        # Blue v Red: Blue wins with 3 over 2
        # Blue v Green: Blue wins with 3 over 2
        # Blue wins all 1v1 contests, so Blue is the condorcet winner
        winner = condorcet_winner(self.candidates, self.tied_plurality)
        self.assertEqual(winner, 'Blue')

        # In a circular loop, all candidates beat one and lose to the other
        winner = condorcet_winner(self.candidates, self.circular_loop)
        self.assertEqual(winner, None)
