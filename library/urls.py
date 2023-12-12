from django.urls import path
from .views import SongListView

urlpatterns = [
    path('library/', SongListView.as_view(), name='library'),
]