from __future__ import unicode_literals

import itertools
import operator

from django.db import models
from django.contrib.auth.models import User

from .ranked_preference import full_ranked_preference


class Option(models.Model):
    label = models.CharField(max_length=128, unique=True)


class Topic(models.Model):
    label = models.CharField(max_length=128, unique=True)
    options = models.ManyToManyField(Option, related_name='topics',
                                     through='TopicOption')

    def calculate_top_options(self, count):
        all_votes = (self.options.order_by('topicoption__rankings__user',
                                           '-topicoption__rankings__score')
                     .values_list('topicoption__rankings__user__id', 'id'))
        all_candidates = self.options.values_list('id', flat=True)

        user_votes = (map(operator.itemgetter(1), votes) for _, votes in
                      itertools.groupby(all_votes, lambda x: x[0]))

        results_generator = full_ranked_preference(all_candidates, user_votes)
        sorted_results = list(itertools.islice(results_generator, count))

        top_results = {obj.id: obj for obj in
                       TopicOption.objects.filter(id__in=sorted_results)}

        return [top_results[id] for id in sorted_results]


class TopicOption(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("option", "topic"),)


class OptionRanking(models.Model):
    topicoption = models.ForeignKey(TopicOption, on_delete=models.CASCADE,
                                    related_name='rankings')
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    score = models.FloatField(default=1000)

    class Meta:
        unique_together = (("topicoption", "user"),)


class Contest(models.Model):
    contestants = models.ManyToManyField(OptionRanking)
    winner = models.ForeignKey(OptionRanking, on_delete=models.CASCADE,
                               null=True, related_name='wins')

    def set_winner(self, winner):
        def elo_expected_score(contestant, opponent):
            score_range = opponent.score - contestant.score
            return 1.0 / (1 + pow(10, score_range / 400))

        assert(self.winner is None)
        assert(winner in self.contestants.all())

        results = [(contestant,
                    contestant == winner,
                    elo_expected_score(contestant, opponent))
                   for contestant, opponent in
                   itertools.permutations(self.contestants.all(), 2)]

        for contestant, is_winner, expected_score in results:
            score = 1 if is_winner else 0
            adjustment = 16 * (score - expected_score)

            contestant.score = models.F('score') + adjustment
            contestant.save()

        self.winner = winner
        self.save()

    @classmethod
    def create_random(cls, topic, user):
        import random
        all_ids = (TopicOption.objects.filter(topic=topic)
                   .values_list('id', flat=True))

        assert(all_ids.count() >= 2)
        contest = Contest.objects.create()
        for topicoption_id in random.sample(all_ids, 2):
            ranking = (OptionRanking.objects
                       .get_or_create(topicoption_id=topicoption_id,
                                      user=user)[0])
            contest.contestants.add(ranking)

        return contest
