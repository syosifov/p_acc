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
        print(serializer.data)
        return serializer.data
    else:
        raise Exception(serializer.error_messages)

@api_view(['GET'])
@transaction.atomic
def db_init(request):
    print("Load data")
    
    
    
    rout = save_acc({})
    section = {}
    section['parent'] = rout['name']
    sub_section = {}
    
    with open("notes.txt", "r") as fp:
        for line in fp:
            line = line[:-1]
            sa = line.split(' | ')
            if len(sa[0]) == 1:
                section['name'] = sa[0]
                section['description'] = sa[1]
                section = save_acc(section)
            elif len(sa[0]) == 2:
                sub_section['name'] = sa[0]
                sub_section['description'] = sa[1]
                sub_section['parent'] = section['name']
                sub_section = save_acc(sub_section)
            else:
                acc = {}
                acc['name'] = sa[0]
                acc['description'] = sa[1]
                match sa[2]:
                    case 'Active': acc['acc_type'] = ACC_A
                    case 'Passive': acc['acc_type'] = ACC_P
                    case _: acc['acc_type'] = ACC_AP
                acc['parent'] = sub_section['name']
                save_acc(acc)
    
    return Response(status=status.HTTP_201_CREATED)
    


# Create your views here.
class AccView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

