from rest_framework.decorators import api_view
from categorizer.models import Category, Topic, Option
from categorizer.serializers import CategorySerializer, TopicSerializer, OptionSerializer
from rest_framework.response import Response


@api_view(['GET'])
def category_list(request, *args, **kwargs):
    categories = Category.objects.all()
    serializer = CategorySerializer(request, categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail(request, *args, **kwargs):
    category = Category.objects.get(id=kwargs['category'])
    serializer = CategorySerializer(request, category)
    return Response(serializer.data)


@api_view(['GET'])
def topic_list(request, *args, **kwargs):
    filters = {
        'category': kwargs['category']
    }
    if 'option' in kwargs:
        filters['options'] = kwargs['option']

    topics = Topic.objects.filter(**filters)
    serializer = TopicSerializer(request, topics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def topic_detail(request, *args, **kwargs):
    topic = Topic.objects.get(id=kwargs['topic'], category=kwargs['category'])
    serializer = TopicSerializer(request, topic)
    return Response(serializer.data)


@api_view(['GET'])
def option_list(request, *args, **kwargs):
    filters = {
        'category': kwargs['category']
    }
    if 'topic' in kwargs:
        filters['topics'] = kwargs['topic']

    options = Option.objects.filter(**filters)
    serializer = OptionSerializer(request, options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def option_detail(request, *args, **kwargs):
    option = Option.objects.get(id=kwargs['option'])
    serializer = OptionSerializer(request, option)
    return Response(serializer.data)
