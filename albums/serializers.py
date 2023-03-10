from xml.etree.ElementInclude import include
from rest_framework import serializers
from .models import Album, Song

class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    
    songs = serializers.SerializerMethodField()
    
    class Meta:
        model = Album
        exclude = ['is_approved']
    
    def get_songs(self, obj, request=None):
        query = Song.objects.filter(album=obj.pk)
        serializer = SongSerializer(query, many=True, context={'request': request})
        return serializer.data    
    
class SongSerializer(serializers.HyperlinkedModelSerializer):
    
    def validate(self, attrs):
        if not attrs.get('name', ''):
            attrs['name'] = attrs['album'].name
        return super().validate(attrs)

    class Meta:
        model = Song
        exclude = ()
        extra_kwargs = {'name': {'required': False}}