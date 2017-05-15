import itertools
from collections import Counter
from operator import itemgetter
import functools


def inlist(l):
    """ Creates a callable that returns true if the value is in l
    """
    def chck(l, v):
        return v in l
    return functools.partial(chck, l)


def firstif(pred, l):
    """ Returns the first value for each item in l that matches the predicate
    """
    for v in l:
        try:
            yield next(itertools.ifilter(pred, v))
        except StopIteration:
            pass


def maxdict(d):
    """ Returns the dictionary key with the largest value
    """
    return max(d.iteritems(), key=itemgetter(1))


def strict_maxdict(d):
    """ Returns the dictionary key with the largest value if only one exists
    """
    items = d.items()
    m = items.pop()
    for tup in items:
        if tup[1] == m[1]:
            m = (None, tup[1])
        elif tup[1] > m[1]:
            m = tup
    return m


def odd_man_out(start):
    """ Generates a tuple for each item paired with every other element.
    For example, ['a', 'b'] becomes [['a', ['b']], ['b', ['a']]]
    """
    for key in start:
        value = list(start)
        value.remove(key)
        yield [key, value]


def instant_runoff(candidates, preferences):
    candidates = set(candidates)
    while candidates:
        top_votes = firstif(inlist(candidates), preferences)
        round_votes = Counter(top_votes)
        total_votes = sum(round_votes.values())
        assert(total_votes > 0)

        (high_candidate, high_votes) = maxdict(round_votes)
        if high_votes > total_votes / 2:
            return high_candidate

        low_votes = min(round_votes.values())
        if low_votes == high_votes:
            # Last remaining candidates are tied
            # Use a set to represent that these candidates are unordered
            return set(round_votes.keys())

        candidates = set(c for (c, v) in round_votes.iteritems()
                         if v > low_votes)
    return None


def condorcet_winner(candidates, preferences):
    def is_condorcet(candidate, opponents, preferences):
        for opponent in opponents:
            votes = firstif(inlist([candidate, opponent]), preferences)
            counts = Counter(votes)
            if counts[candidate] <= counts[opponent]:
                # Can't be a condorcet winner if a opponent received more votes
                return False
        # No opponent had more votes, therefore this is a condorcet winer
        return True

    for candidate, opponents in odd_man_out(candidates):
        if is_condorcet(candidate, opponents, preferences):
            return candidate
    return None


def pairwise_rankings(candidates, preferences):
    # Get a list of all candidate combinations
    pairs = itertools.combinations(candidates, 2)

    # For each pair, build a list of who got the higher vote
    pair_votes = (firstif(inlist(pair), preferences) for pair in pairs)

    # Count the votes and pick the winner
    tallies = (Counter(votes) for votes in pair_votes)
    winners = (strict_maxdict(tally)[0] for tally in tallies if tally)

    # Count who won how many pairings and sort by their wins
    final_tally = Counter(winners)
    results = sorted(final_tally.keys(), key=final_tally.get,
                     reverse=True)
    for k, group in itertools.groupby(results, final_tally.get):
        group = list(group)
        if len(group) == 1:
            yield group[0]
        else:
            yield set(group)


def full_ranked_preference(candidates, preferences):
    preferences = list(preferences)
    candidates = list(candidates)
    while candidates:
        try:
            v = instant_runoff(candidates, preferences)
        except AssertionError:
            return

        yield v
        try:
            candidates.remove(v)
        except ValueError:
            candidates = list(itertools.ifilterfalse(inlist(v), candidates))
