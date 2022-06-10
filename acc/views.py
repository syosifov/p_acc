from django.db import transaction

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Account, ACC_A, ACC_P, ACC_AP
from .serializers import AccountSerializer

def save_acc(acc):
    serializer = AccountSerializer(data=acc)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise Exception(serializer.error_messages)

@api_view(['GET'])
@transaction.atomic
def db_init(request):
    print("Load data")
    
    
    
    rout = save_acc({})
    section = {}
    section['name'] = '10'
    section['description'] = 'Capital'
    section['parent'] = ' '
    section = save_acc(section)
    
    sub_section = {}
    sub_section['name'] = 104
    sub_section['description'] = 'Capital of non - profit enterprises'
    sub_section['acc_type'] = ACC_P
    sub_section['parent'] = section['name']
    sub_section = save_acc(sub_section)
    # with open("notes.txt", "r") as fp:
    #     for line in fp:
    #         line = line[:-1]
    #         sa = line.split(' | ')
    #         print(sa)
    #         print(len(sa))
    
    return Response(status=status.HTTP_201_CREATED)
    


# Create your views here.
class AccView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

