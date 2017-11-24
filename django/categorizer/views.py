from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework import viewsets

from categorizer.models import (Topic, Option, TopicOption, Contest,
                                OptionRanking)
from categorizer.serializers import TopicSerializer, OptionSerializer


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


class OptionViewSet(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()

    def get_queryset(self):
        queryset = Option.objects.all()
        try:
            topic_id = self.request.query_params['topic']
            queryset = queryset.filter(topics__id=topic_id)
        except KeyError:
            pass

        return queryset


@api_view(['GET', 'DELETE', 'PUT'])
def topic_option_detail(request, topic_id, option_id):
    if request.method == 'PUT':
        topic = get_object_or_404(Topic, id=topic_id)
        option = get_object_or_404(Option, id=option_id)
        mapping = TopicOption.objects.create(
            topic=topic,
            option=option
        )
        return Response({
            'status': 'created'
        }, status=HTTP_201_CREATED)

    # For GET or DELETE, a TopicOption object must aleady exist
    mapping = get_object_or_404(TopicOption, topic__id=topic_id,
                                option__id=option_id)
    if request.method == 'GET':
        return Response({
            'status': 'OK'
        })
    elif request.method == 'DELETE':
        mapping.delete()
        return Response({
            'status': 'deleted'
        })


@api_view(['GET', 'POST', 'DELETE'])
def contest_manager(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    try:
        contest = topic.contests.distinct().get(
            user=request.user,
            winner__isnull=True
        )
    except Contest.DoesNotExist:
        if request.method == 'GET':
            contest = Contest.create_random(topic=topic, user=request.user)
        else:
            raise

    if request.method == 'GET':
        contestants = Option.objects.filter(
            topicoption__rankings__in=contest.contestants.all())
        serialized = OptionSerializer(contestants, many=True)
        return Response(serialized.data)

    if request.method == 'POST':
        winning_id = request.POST['winner']
        try:
            winner = contest.contestants.get(topicoption__option_id=winning_id)
        except OptionRanking.DoesNotExist:
            raise ParseError('Unknown winner')

        contest.set_winner(winner)
    elif request.method == 'DELETE':
        contest.delete()

    return Response({
        'status': 'OK'
    })


@api_view(['GET'])
def topic_rankings(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    count = int(request.GET.get('count', 5))
    top_n = topic.calculate_top_options(count)

    serialized = OptionSerializer(top_n, many=True)
    return Response(serialized.data)
