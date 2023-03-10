from logging import exception
from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.core import exceptions
from model_utils.models import TimeStampedModel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.

class Album(TimeStampedModel):
    
    name = models.CharField(max_length=200, blank=False, null=False)
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE)   
    release_date = models.DateTimeField(blank=False)
    cost = models.FloatField(default=0.0, validators=[MinValueValidator(0, message="Cost must be a non-negative value.")], blank=False)
    is_approved = models.BooleanField("Approve the album if its name is not explicit", default=False)
    
    def __str__(self):
        return "{name}, {artist}".format(name=self.name, artist=self.artist.name)
    
class Song(TimeStampedModel):
    
    name = models.CharField(max_length=200, blank=False, null=False)
    album = models.ForeignKey('albums.Album', on_delete=models.CASCADE)   
    image = models.FileField(upload_to='uploads', validators=[FileExtensionValidator(['jpeg', 'jpg', 'jpe', 'jfif'])])
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(100, 50)], format='JPEG', options={'quality': 60})
    audio = models.FileField(upload_to='uploads', validators=[FileExtensionValidator(['mp3', 'wav'])])
    
    def isOnlySong(self):
        return self.album.song_set.all().count()==1
    
    def delete(self):
        if self.isOnlySong():
            raise exceptions.BadRequest("Cannot delete the song {}, because its {}'s only song.".format(self.name, self.album.name))
        return super().delete()
        
    def __str__(self):
        return "{name}, {album}".format(name=self.name, album=self.album.name)