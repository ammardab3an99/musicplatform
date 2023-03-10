from django.shortcuts import render
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from .models import ExUser
from .serializers import ExUserSerializer

# Create your views here.
class ExUserViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    
    queryset = ExUser.objects.all()
    serializer_class = ExUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def delete(self, request, *args, **kwargs):
        if (request.user.username!='admin') and (self.kwargs['pk'] != str(request.user.pk)):
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if (request.user.username!='admin') and (self.kwargs['pk'] != str(request.user.pk)):
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)
    
    