from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status, viewsets

from .utils import createSubscriber, аssign1Data, subsInit, testSubscribeTax, testAssignTax
from .models import Tax, AssignedTax, Subscriber
from .serializers import TaxSerializer, AssignedTaxSerializer, SubscriberSerializer

# Create your views here.


@api_view(['POST'])     # subs/create_subscriber/
def create_subscriber(request):
   
    try:
        with transaction.atomic():
            ad = request.data
            parent = ad['parent']
            suffix = ad['suffix']
            start = ad['start']
            end = ad['end']         # inclusive
            createSubscriber(parent, suffix, start, end)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


class TaxView(viewsets.ModelViewSet):       # subs/tax/
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


@api_view(['POST'])     # subs/subscribe_tax/
def subscribe_tax(request):             # TODO to define interface
    testSubscribeTax()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])     # subs/assign_tax
def assign_tax(request):
    
    tax = Tax.objects.all()[0]
    qs = Subscriber.objects.filter(name__startswith='g001a')
    try:
        with transaction.atomic():
            testAssignTax(tax)
            # raise Exception('Test exception')
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])     # subs/init/
def init(request):
    try:
        subsInit(request)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)
