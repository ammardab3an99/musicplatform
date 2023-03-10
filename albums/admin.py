from logging import exception
from django import forms
from django.contrib import admin, messages
from .models import Album, Song


class SongInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        # Check that at least one service has been entered.
        super(SongInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(e and not e.get('DELETE', False) for e in self.cleaned_data):
            raise forms.ValidationError('At least one song is required.')


class SongInline(admin.TabularInline):
    model = Song
    formset = SongInlineFormSet


class SongAdminForm(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data['name'] or self.cleaned_data['album'].name

    class Meta:
        model = Song
        exclude = ()
        widgets = {
            'image': forms.FileInput(attrs={'accept': '.jpeg, .jpg, .jpe, .jfif'}),
            'audio': forms.FileInput(attrs={'accept': '.mp3, .wav'}),
        }


class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['is_approved'].help_text = 'Approve the album if its name is not explicit'

    class Meta:
        model = Album
        exclude = ()


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    list_display = ('name', 'artist', 'release_date')
    readonly_fields = ('created', 'modified')
    inlines = [SongInline]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    form = SongAdminForm
    list_display = ('name', 'album', 'image_thumbnail')
    readonly_fields = ('created', 'modified')

    def delete_queryset(self, request, queryset):
        for song in queryset.all():
            try:
                song.delete()
            except Exception as e:
                messages.error(request, e.message)

    def has_delete_permission(self, request, obj=None):
        return not obj or not obj.isOnlySong()
