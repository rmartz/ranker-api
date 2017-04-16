from django.db.models.signals import pre_delete
from django.dispatch import receiver
from categorizer.models import OptionRanking, Contest


@receiver(pre_delete, sender=OptionRanking)
def on_option_ranking_delete(sender, instance, **kwargs):
    # If an OptionRanking is deleted for whatever reason, delete any contests
    # that it belonged to since they are no longer meaningful.
    Contest.objects.filter(contestants=instance).delete()
