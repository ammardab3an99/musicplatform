from rest_framework import serializers
from .models import Artist
from albums.models import Album
from albums.serializers import AlbumSerializer

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    
    albums = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = ('id', 'url', 'name', 'social_media_link', 'albums')
        
    def get_albums(self, obj, request=None):
        query = Album.objects.filter(artist=obj.pk)
        serializer = AlbumSerializer(query, many=True, context={'request': request})
        return serializer.data