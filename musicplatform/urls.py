from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from rest_framework import routers
from artists.views import ArtistViewSet
from albums.views import AlbumViewSet, SongViewSet
from users.views import ExUserViewSet

router = routers.DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'users', ExUserViewSet)

urlpatterns = [
    
    path('', include(router.urls)),
    path('auth/', include('authentication.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
