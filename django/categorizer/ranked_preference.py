from itertools import ifilter, ifilterfalse
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
            yield next(ifilter(pred, v))
        except StopIteration:
            pass


def maxdict(d):
    """ Returns the dictionary key with the largest value
    """
    return max(d.iteritems(), key=itemgetter(1))


def instant_runoff(candidates, preferences):
    candidates = set(candidates)
    while candidates:
        top_votes = firstif(inlist(candidates), preferences)
        round_votes = Counter(top_votes)
        total_votes = sum(round_votes.values())
        (high_candidate, high_votes) = maxdict(round_votes)
        if high_votes > total_votes / 2:
            return high_candidate

        low_votes = min(round_votes.values())
        if low_votes == high_votes:
            # Last remaining candidates are tied
            return candidates

        candidates = set(c for (c, v) in round_votes.iteritems() if v > low_votes)
    return None


def full_ranked_preference(candidates, preferences):
    preferences = list(preferences)
    candidates = list(candidates)
    while candidates:
        v = instant_runoff(candidates, preferences)
        yield v
        try:
            candidates.remove(v)
        except ValueError:
            candidates = list(ifilterfalse(inlist(v), candidates))
