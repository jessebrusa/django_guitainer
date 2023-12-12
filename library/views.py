from django.views.generic import ListView
from .models import Song

class SongListView(ListView):
    model = Song
    template_name = 'base/library.html' 
    context_object_name = 'song_list'