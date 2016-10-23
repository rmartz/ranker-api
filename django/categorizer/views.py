from rest_framework.decorators import api_view
from categorizer.models import Category
from categorizer.serializers import CategorySerializer
from rest_framework.response import Response


@api_view(['GET'])
def category_list(request, *args, **kwargs):
    categories = Category.objects.all()
    serializer = CategorySerializer(request, categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail(request, *args, **kwargs):
    category = Category.objects.get(id=kwargs['id'])
    serializer = CategorySerializer(request, category)
    return Response(serializer.data)
