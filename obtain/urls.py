from django.urls import path
from .views import *

urlpatterns = [
    path('find-song', MyFormView.as_view(), name='find-song'),

    path('song-search/', SongSearchView.as_view(), name='song-search-view'),
    path('correct-title-artist', CorrectTitleArtist.as_view(), name='correct-title-artist'),
    path('obtain-img/', ObtainImgView.as_view(), name='obtain-img'),
    path('obtain-lyrics/', ObtainLyricsView.as_view(), name='obtain-lyrics'),
    path('obtain-mp3/', ObtainMp3View.as_view(), name='obtain-mp3'),
    path('obtain-karaoke/', ObtainKaraokeView.as_view(), name='obtain-karaoke'),
]
