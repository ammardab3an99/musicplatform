from django import forms
from django.core.validators import FileExtensionValidator, MinValueValidator
from .models import Album, Song


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class NewAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        widgets = {'release_date': DateTimePickerInput}
        exclude = ['is_approved']


class NewSongForm(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data['name'] or self.cleaned_data['album'].name

    class Meta:
        model = Song
        exclude = ()
        widgets = {
            'image': forms.FileInput(attrs={'accept': '.jpeg, .jpg, .jpe, .jfif'}),
            'audio': forms.FileInput(attrs={'accept': '.mp3, .wav'}),
        }
