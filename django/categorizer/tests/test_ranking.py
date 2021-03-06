from django.test import TestCase
from categorizer.ranked_preference import (instant_runoff, pairwise_rankings,
                                           full_ranked_preference,
                                           condorcet_winner)


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
            ['Red'],
            ['Red'],
            ['Red'],
            ['Yellow', 'Red'],
            ['Yellow', 'Red'],
            ['Blue'],
            ['Blue'],
            ['Blue'],
            ['Blue']
        ]
        self.partisan_split = [
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
        self.simple_tie = [
            ['Red'],
            ['Blue']
        ]
        self.circular_loop = [
            ['Red', 'Blue', 'Green'],
            ['Blue', 'Green', 'Red'],
            ['Green', 'Red', 'Blue']
        ]


class InstantRunoffTestCase(RankedPreferenceTestCase):
    def test_tied_plurality(self):
        # Round 1: Red gets only 1 vote, drops out
        # Round 2: Blue gets 3 votes, wins
        winner = instant_runoff(self.candidates, self.tied_plurality)
        self.assertEqual(winner, 'Blue')

    def test_partisan_split(self):
        # Round 1: Red gets only 1 vote, drops out
        # Round 2: Green gets only 2 votes, drops out
        # Round 3: Yellow gets 5 votes, wins
        winner = instant_runoff(self.candidates, self.partisan_split)
        self.assertEqual(winner, 'Yellow')

    def test_spoiler_effect(self):
        # Round 1: Yellow drops out
        # Round 2: Red wins
        winner = instant_runoff(self.candidates, self.spoiler_effect)
        self.assertEqual(winner, 'Red')

    def test_simple_tie(self):
        winner = instant_runoff(self.candidates, self.simple_tie)
        self.assertItemsEqual(winner, ['Red', 'Blue'])

    def test_circular_loop(self):
        # In a circular loop, all candidates tie first round
        winner = instant_runoff(self.candidates, self.circular_loop)
        self.assertItemsEqual(winner, ['Red', 'Blue', 'Green'])

    def test_single_voter(self):
        winner = instant_runoff(self.candidates, [self.candidates])
        # Only one voter, so winner should be first candidate
        self.assertEqual(winner, self.candidates[0])


class FullRankedPreferenceTestCase(RankedPreferenceTestCase):
    def test_tied_plurality(self):
        # Round 1: Red gets only 1 vote, drops out
        # Round 2: Blue gets 3 votes, wins 1st place
        # Repeat without Blue
        # Round 1: Green gets 3 votes, wins 2nd place
        # Repeat without Blue or Green
        # Round 1: Red gets 5 votes, wins 3rd place
        winners = list(full_ranked_preference(self.candidates,
                                              self.tied_plurality))
        self.assertEqual(winners, ['Blue', 'Green', 'Red'])

    def test_partisan_split(self):
        # Yellow wins 1st place
        # Repeat without Yellow
        # Round 1: Green gets only 2 votes, dops out
        # Round 2: Red gets 5 votes, wins 2nd place
        # Repeat without Yellow or Red
        # Round 1: Blue gets 4 votes, wins 3rd place
        # Repeat without Yellow, Red or Blue
        # Round 1: Green gets 3 votes, wins 4th place
        winner = list(full_ranked_preference(self.candidates,
                                             self.partisan_split))
        self.assertEqual(winner, ['Yellow', 'Red', 'Blue', 'Green'])

    def test_spoiler_effect(self):
        # Round 1: Yellow drops out
        # Round 2: Red wins
        # Repeat without Red
        # Round 1: Blue wins
        # Repeat without Blue
        # Round 1: Yellow wins
        winner = list(full_ranked_preference(self.candidates,
                                             self.spoiler_effect))
        self.assertEqual(winner, ['Red', 'Blue', 'Yellow'])

    def test_simple_tie(self):
        winner = list(full_ranked_preference(self.candidates, self.simple_tie))
        self.assertItemsEqual(winner, [set(['Red', 'Blue'])])

    def test_circular_loop(self):
        # In a circular loop, all candidates tie first round
        winner = list(full_ranked_preference(self.candidates,
                                             self.circular_loop))
        self.assertItemsEqual(winner, [set(['Red', 'Blue', 'Green'])])

    def test_single_voter(self):
        winner = list(full_ranked_preference(self.candidates, [self.candidates]))
        # Only one voter, so results should be order voter selected
        self.assertEqual(winner, self.candidates)


class CondorcetWinnerTestCase(RankedPreferenceTestCase):
    def test_tied_plurality(self):
        # Red v Green: Green wins with 3 over 2
        # Blue v Red: Blue wins with 3 over 2
        # Blue v Green: Blue wins with 3 over 2
        # Blue wins all 1v1 contests, so Blue is the condorcet winner
        winner = condorcet_winner(self.candidates, self.tied_plurality)
        self.assertEqual(winner, 'Blue')

    def test_partisan_split(self):
        winner = condorcet_winner(self.candidates, self.partisan_split)
        self.assertEqual(winner, 'Yellow')

    def test_spoiler_effect(self):
        winner = condorcet_winner(self.candidates, self.spoiler_effect)
        self.assertEqual(winner, 'Red')

    def test_simple_tie(self):
        winner = condorcet_winner(self.candidates, self.simple_tie)
        self.assertEqual(winner, None)

    def test_circular_loop(self):
        # In a circular loop, all candidates beat one and lose to the other
        winner = condorcet_winner(self.candidates, self.circular_loop)
        self.assertEqual(winner, None)

    def test_single_voter(self):
        winner = condorcet_winner(self.candidates, [self.candidates])
        # Only one voter, so winner should be the first candidate
        self.assertEqual(winner, self.candidates[0])


class PairwiseRankingsTestCase(RankedPreferenceTestCase):
    def test_tied_plurality(self):
        winners = list(pairwise_rankings(self.candidates, self.tied_plurality))
        self.assertEqual(winners, ['Blue', 'Green', 'Red', 'Yellow'])

    def test_partisan_split(self):
        winners = list(pairwise_rankings(self.candidates, self.partisan_split))
        self.assertEqual(winners, ['Yellow', 'Red', 'Blue', 'Green'])

    def test_spoiler_effect(self):
        winners = list(pairwise_rankings(self.candidates, self.spoiler_effect))
        self.assertEqual(winners, ['Red', 'Blue', 'Yellow', 'Green'])

    def test_simple_tie(self):
        winner = list(pairwise_rankings(self.candidates, self.simple_tie))
        # Red and Blue are tied for first place, with 2 wins each, Green and
        # Yellow are tied for third place with 0 wins each
        self.assertEqual(winner, [set(['Red', 'Blue']),
                                  set(['Green', 'Yellow'])])

    def test_single_voter(self):
        winner = list(pairwise_rankings(self.candidates, [self.candidates]))
        # Only one voter, so results should be order voter selected
        self.assertEqual(winner, self.candidates)

    def test_circular_loop(self):
        # In a circular loop, all candidates beat one and lose to the other
        winner = list(pairwise_rankings(self.candidates, self.circular_loop))
        self.assertEqual(winner, [set(['Red', 'Blue', 'Green']), 'Yellow'])
