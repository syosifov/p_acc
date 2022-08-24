from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


@api_view(['POST'])
def fn_template(request):
    try:
        with transaction.atomic():
            pass
        # raise Exception("Test exception")
    except Exception as e:
        print(str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)
