from rest_framework import serializers, exceptions
from .models import ExUser
from django.contrib.auth.hashers import make_password

class ExUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ExUser
        fields = ('id', 'url', 'username', 'email', 'bio')