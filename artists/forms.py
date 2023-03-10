from django import forms
from .models import Artist


class NewArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        exclude = ()
