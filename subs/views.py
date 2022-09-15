from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets

from .utils import (subsInit, 
                    testSubscribeTax, 
                    testAssignTax,
                    payTax,
                    importMoney)
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
            # createSubscriber(parent, suffix, start, end)
            raise Exception('Test exception')
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


class TaxView(viewsets.ModelViewSet):       # subs/tax/
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


@api_view(['POST'])     # subs/subscribe_tax/
def subscribe_tax(request):             # TODO to define interface
    with transaction.atomic():
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
        with transaction.atomic():
            subsInit(request)
            # page = request.data['PAGE']
        # raise Exception("Test exception")
    except Exception as e:
        print(str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])     # subs/unpaid/
def unpaid(request):
    try:
        a_taxes = AssignedTax.objects.filter(paid=False)
        at_serializer = AssignedTaxSerializer(data=a_taxes, many=True)
        at_serializer.is_valid()
    except Exception as e:
        print(str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(at_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])     # subs/pay/
def pay(request):
    try:
        with transaction.atomic():
            assigned_tax_id = int(request.data['assigned_tax_id'])
            payTax(assigned_tax_id)
            # raise Exception("Test exception")
    except Exception as e:
        print(str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])         # subs/installment/
def installment(request):
    try:
        with transaction.atomic():
            subscriber_id = request.data['subscriber_id']
            amount = (request.data['amount'])
            description = request.data['description']
            importMoney(subscriber_id,amount,description)
            # raise Exception("Test exception")
    except Exception as e:
        print(str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)



@api_view(['POST'])
def test(request):

    try:
        with transaction.atomic():
            pass
            # raise Exception("Test exception")
    except Exception as e:
        print(str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)
