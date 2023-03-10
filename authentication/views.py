from rest_framework import permissions, generics, status, views
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.contrib.auth import login, logout
from django.contrib.auth.signals import user_logged_out
from knox.models import AuthToken
from users.models import ExUser
from users.serializers import ExUserSerializer
from .serializers import RegisterUserSerializer, LoginUserSerializer
class RegisterUserView(generics.CreateAPIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer
    
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            newUser = serializer.data
            ExUser.objects.create_user(newUser['username'], newUser['email'], newUser['password1'])
            return Response({'success': True})
        else:
            return Response({'success': False, 'errors': serializer.errors})

class LoginUserView(generics.CreateAPIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginUserSerializer
    
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        user_serialized_data = ExUserSerializer(user, context={'request': request}).data
        token =  AuthToken.objects.create(user)[1]
        login(request, user)
        return Response({'success': True, 'token': token, 'user': user_serialized_data}, status=status.HTTP_202_ACCEPTED)
    
class LogoutUserView(views.APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    
    def post(self, request, format=None):
        logout(request)
        if request._auth:
            request._auth.delete()
        user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    