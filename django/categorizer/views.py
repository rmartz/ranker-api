from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from categorizer.models import (Topic, Option, TopicOption, Contest,
                                OptionRanking)
from categorizer.serializers import (TopicSerializer, OptionSerializer,
                                     ContestSerializer)


@api_view(['GET', 'POST'])
def topic_list(request):
    if request.method == 'GET':
        topics = Topic.objects.all().values('id', 'label')
        serialized = TopicSerializer(topics, many=True)
        return Response(serialized.data)
    elif request.method == 'POST':
        label = request.POST['label']
        topic = Topic.objects.create(label=label)
        return Response({
            'id': topic.id,
            'status': 'created'
        })


@api_view(['GET', 'DELETE', 'POST'])
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'GET':
        serialized = TopicSerializer(topic)
        return Response(serialized.data)
    elif request.method == 'DELETE':
        topic.delete()
        return Response({
            'status': 'deleted'
        })
    elif request.method == 'POST':
        topic.label = request.POST['label']
        topic.save()
        return Response({
            'id': topic.id,
            'status': 'updated'
        })


@api_view(['GET', 'POST'])
def option_list(request):
    if request.method == 'GET':
        options = Option.objects.all().values('id', 'label')
        serialized = OptionSerializer(options, many=True)
        return Response(serialized.data)
    elif request.method == 'POST':
        label = request.POST['label']
        option = Option.objects.create(label=label)
        return Response({
            'id': option.id,
            'status': 'created'
        })


@api_view(['GET', 'DELETE', 'POST'])
def option_detail(request, option_id):
    option = get_object_or_404(Option, id=option_id)
    if request.method == 'GET':
        serialized = OptionSerializer(option)
        return Response(serialized.data)
    elif request.method == 'DELETE':
        option.delete()
        return Response({
            'status': 'deleted'
        })
    elif request.method == 'POST':
        option.label = request.POST['label']
        option.save()
        return Response({
            'id': option.id,
            'status': 'updated'
        })


@api_view(['GET'])
def topic_option_list(request, topic_id):
    options = (Option.objects.filter(topicoption__topic__id=topic_id)
               .values('id', 'label'))
    serialized = OptionSerializer(options, many=True)
    return Response(serialized.data)


@api_view(['GET', 'DELETE', 'PUT'])
def topic_option_detail(request, topic_id, option_id):
    if request.method == 'PUT':
        mapping = TopicOption.objects.create(
            topic_id=topic_id,
            option_id=option_id
        )
        return Response({
            'status': 'created'
        })

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


@api_view(['GET', 'POST'])
def contest_manager(request, topic_id):
    try:
        contest = Contest.objects.distinct().get(
            contestants__user=request.user,
            contestants__topicoption__topic_id=topic_id,
            winner__isnull=True
        )
    except Contest.DoesNotExist:
        contest = Contest.create_random(topic=topic_id, user=request.user)

    if request.method == 'GET':
        contestants = Option.objects.filter(
            topicoption__rankings__in=contest.contestants.all())
        serialized = OptionSerializer(contestants, many=True)
        return Response(serialized.data)
    elif request.method == 'POST':
        winning_id = request.POST['winner']
        try:
            winner = contest.contestants.get(topicoption__option_id=winning_id)
        except OptionRanking.DoesNotExist:
            raise ParseError()

        contest.set_winner(winner)
        return Response({
            'status': 'OK'
        })


@api_view(['GET'])
def topic_rankings(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    count = request.GET.get('count', 5)
    top_n = topic.calculate_top_options(count)

    serialized = OptionSerializer(top_n, many=True)
    return Response(serialized.data)
