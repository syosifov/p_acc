from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status, viewsets

from .utils import createSubscriber
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
    
    
    