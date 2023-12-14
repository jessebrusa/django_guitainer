from django.urls import path
from .views import LibraryView, CatalogueView, SongDetailView, AddToLibraryView, RemoveFromLibraryView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('library/', LibraryView.as_view(), name='library'),
    path('catalogue/', CatalogueView.as_view(), name='catalogue'),
    path('song/<int:pk>/', SongDetailView.as_view(), name='song_detail'),

    path('add-to-library/<int:song_id>/', AddToLibraryView.as_view(), name='add_to_library'),
    path('remove-from-library/<int:song_id>/', RemoveFromLibraryView.as_view(), name='remove_from_library'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)