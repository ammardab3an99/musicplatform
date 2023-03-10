from django.contrib.auth import password_validation
from rest_framework import serializers, validators
from users.models import ExUser
from django.contrib.auth import authenticate

class RegisterUserSerializer(serializers.Serializer):
    
    username = serializers.CharField(required=True, max_length=200, validators=[validators.UniqueValidator(queryset=ExUser.objects.all())])
    email = serializers.EmailField(required=True, max_length=200)
    password1 = serializers.CharField(required=True, max_length=200, trim_whitespace=False)
    password2 = serializers.CharField(required=True, max_length=200, trim_whitespace=False)
    
    def validate(self, data):
        
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        
        if (not username) or (not email) or (not password1) or (not password2):
            return data
        
        if password1 != password2:
            raise serializers.ValidationError('the given passwords are not equal.')
        else:
            user = ExUser(username=username, email=email)
            password_validation.validate_password(password1, user)
        
        return data
        

class LoginUserSerializer(serializers.Serializer):
    
    username = serializers.CharField(required=True, max_length=200, write_only=True)
    password = serializers.CharField(required=True, max_length=200, trim_whitespace=False, write_only=True)
    
    def validate(self, data):
        
        username = data.get('username')
        password = data.get('password')
    
        if (not username) or (not password):
            return data
        
        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:
            msg = 'Access denied: wrong username or password.'
            raise serializers.ValidationError(msg, code='authorization')
        
        data['user'] = user
        return data