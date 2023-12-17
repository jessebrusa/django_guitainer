from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('library/', LibraryView.as_view(), name='library'),
    path('catalogue/', CatalogueView.as_view(), name='catalogue'),
    path('song/<int:pk>/', SongDetailView.as_view(), name='song-detail'),

    path('add-to-library/<int:song_id>/', AddToLibraryView.as_view(), name='add-to-library'),
    path('remove-from-library/<int:song_id>/', RemoveFromLibraryView.as_view(), name='remove-from-library'),

    path('add-remove-favorite/', AddRemoveFavoritesView.as_view(), name='add-remove-favorite'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)