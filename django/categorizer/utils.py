from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    if exc.__class__ == AssertionError:
        return Response({'assertion': 'FAILED'},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return exception_handler(exc, context)
