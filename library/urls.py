from django.urls import path
from .views import LibraryView, CatalogueView, SongDetailView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('library/', LibraryView.as_view(), name='library'),
    path('catalogue/', CatalogueView.as_view(), name='catalogue'),
    path('song/<int:pk>/', SongDetailView.as_view(), name='song_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)