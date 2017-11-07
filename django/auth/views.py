from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_admin(request):
    if request.method == 'POST':
        # Create a new user account
        user_class = get_user_model()
        user = user_class.objects.create_user(
            request.POST['username'],
            request.POST['email'],
            request.POST['password'])
        token = Token.objects.create(user=user)

        return Response({'token': token.key}, status=HTTP_201_CREATED)


@api_view(['POST', 'DELETE'])
@permission_classes((AllowAny, ))
def token_admin(request):
    user = authenticate(username=request.POST['username'],
                        password=request.POST['password'])
    if user is None:
        return Response({'data': 'Authentication failed'},
                        status=HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        # Reset the API token and provide a new one
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
    elif request.method == 'POST':
        token = Token.objects.get(user=user)

    return Response({'token': token.key})
