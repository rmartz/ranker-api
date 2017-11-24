from rest_framework import serializers

from categorizer.models import Topic, Option, Contest


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'label')


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'label')


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('contestants', )
