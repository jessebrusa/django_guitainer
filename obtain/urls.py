from django.urls import path
from .views import MyFormView, SongSearchView, CorrectTitleArtist

urlpatterns = [
    path('find-song', MyFormView.as_view(), name='find-song'),

    path('song-search/<str:song_title>', SongSearchView.as_view(), name='song-search-view'),
    path('correct-title-artist', CorrectTitleArtist.as_view(), name='correct-title-artist'),
]
