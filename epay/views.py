from django.shortcuts import render
from django.db import transaction
from decimal import Decimal

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets

from .utils import prepare_payment

# Create your views here.


@api_view(['POST','GET'])   # /epay/test/
def test(request):

    try:
        with transaction.atomic():
            r = prepare_payment('D460900632',Decimal(10),'Тестово плащане','001000002',60*60)
            # raise Exception("Test exception")
    except Exception as e:
        print(str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(r, status=status.HTTP_201_CREATED)

