from django.contrib import admin
from .models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):

    def approvedAlbums(self, obj):
        result = obj.album_set.filter(is_approved=True).count()
        return result

    approvedAlbums.short_description = "Approved Albums"
    approvedAlbums.admin_order_field = 'approved_albums'

    list_display = ('name', 'social_media_link', 'approvedAlbums')
    readonly_fields = ('created', 'modified')

    model = Artist
