from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from categorizer.models import Topic
from categorizer.serializers import TopicSerializer


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
            'id': int(topic_id),
            'status': 'deleted'
        })
    elif request.method == 'POST':
        topic.label = request.POST['label']
        topic.save()
        return Response({
            'id': topic.id,
            'status': 'updated'
        })
