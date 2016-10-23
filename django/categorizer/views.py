from rest_framework.decorators import api_view
from categorizer.models import Category
from categorizer.serializers import CategorySerializer
from rest_framework.response import Response


@api_view(['GET'])
def category_list(request, *args, **kwargs):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category(request, *args, **kwargs):
    category = Category.objects.get(id=kwargs['id'])
    serializer = CategorySerializer(category)
    return Response(serializer.data)
