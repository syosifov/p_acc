from django.db import transaction
from django.db.models.signals import post_save

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers

from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "groups",
            "user_permissions"
        ]

# https://www.django-rest-framework.org/api-guide/authentication/
class CustomAuthToken(ObtainAuthToken):     # login/

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        groups = user.groups;
        print(list(groups.all().values('name')))
        user_serializer = UserSerializer(user)
        data = user_serializer.data
        data['token'] = token.key
        data['all_permissions'] = list(user.get_all_permissions())
        return Response(data=data,status=status.HTTP_200_OK)
 
        
@api_view(['POST'])         # signup/
@permission_classes([AllowAny])
def signUp(request):
    try:
        with transaction.atomic():
            user = User()
            user.set_password(request.data['password'])
            user.username = request.data['username']
            user.email = request.data['email']
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.save()
            token = Token.objects.get(user_id=user.id)
            user_serializer = UserSerializer(user)
            data = user_serializer.data
            data['token'] = token.key
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST) 
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])          # logout/
def logout(request):

    user = request.user
    token = Token.objects.get(user=user)
    token.delete()
    return Response(status=status.HTTP_200_OK)


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def createtAuthToken(sender,instance,created,**kwargs):
    
    if created:
        Token.objects.create(user=instance)