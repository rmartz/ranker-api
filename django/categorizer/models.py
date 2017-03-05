from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Option(models.Model):
    label = models.CharField(max_length=128, unique=True)


class Topic(models.Model):
    label = models.CharField(max_length=128, unique=True)
    options = models.ManyToManyField(Option, related_name='topics',
                                     through='TopicOption')

    def calculate_top_options(self, count):
        for user in self.options_set.values('rankings__user').distinct():
            votes = (self.options_set.filter(rankings__user=user)
                     .order_by('-ranking__score'))

            raise Exception(votes)

        return self.options.order_by(models.Avg('rankings__score'))[:count]


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
        assert(self.winner is None)
        assert(winner in self.contestants.all())

        for contestant, opponent in [(self.contestants.all().order_by('id')),
                                     (self.contestants.all().order_by('-id'))]:
            score = 1 if contestant is winner else 0
            rating_gap = opponent.score - contestant.score
            expected = 1.0 / (1 + pow(10, rating_gap / 400))

            adjustment = 16 * (score - expected)

            contestant.score = models.F('score') + adjustment
            contestant.save()

        self.winner = winner
        self.save()

    @classmethod
    def create_random(cls, topic, user):
        import random
        all_ids = (TopicOption.objects.filter(topic=topic)
                   .values_list('id', flat=True))

        contest = Contest.objects.create()
        for topicoption_id in random.sample(all_ids, 2):
            ranking = (OptionRanking.objects
                       .get_or_create(topicoption_id=topicoption_id,
                                      user=user)[0])
            contest.contestants.add(ranking)

        return contest
