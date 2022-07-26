from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status, viewsets

from .utils import createSubscriber, аssign1Data
from .models import Tax, AssignedTax, Subscriber
from .serializers import TaxSerializer, AssignedTaxSerializer, SubscriberSerializer

# Create your views here.


@api_view(['POST'])     # subs/create_subscriber/
def create_subscriber(request):
    # {
    #     "parent": "g001",
    #     "suffix": "a",
    #     "start": 1,
    #     "end": 4
    # }

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
    taxes = Tax.objects.all()
    qs = Subscriber.objects.all()
    print(qs[0])
    for s in qs:
        if s.name.find('a') < 0:
            continue
        lst = s.name.split('a')
        n = int(lst[len(lst)-1])
        if n % 2 == 0:
            s.taxes.add(taxes[0])
        else:
            s.taxes.add(taxes[1])
        print(s)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])     # subs/assign_tax
def assign_tax(request):
    detail = request.data['assignment_name']
    # '2022.07'
    tax = Tax.objects.all()[0]
    qs = Subscriber.objects.filter(name__startswith='g001a')
    try:
        with transaction.atomic():
            for subscriber in qs:
                taxes = subscriber.taxes.all()
                
                if tax in taxes:
                    description = f'{subscriber.name} - {tax.name} - {detail}'
                    assignedTaxes = subscriber.assignedTaxes.filter(description=description)
                    if(len(assignedTaxes) > 0):
                        continue
                    at = AssignedTax(tax=tax, amount=tax.amount, description=description)
                    at.save()
                    subscriber.assignedTaxes.add(at)
                    subscriber.save()
                    assign_id = аssign1Data(subscriber.account.name,
                                            '712',
                                            tax.amount,
                                            description)
                    at.assign_debit_id = assign_id
                    at.save()
                    # raise Exception('Test exception')
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)
