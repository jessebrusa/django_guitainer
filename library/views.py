from django.views.generic import ListView, DetailView
from .models import Song

class LibraryView(ListView):
    model = Song
    template_name = 'base/library.html' 
    context_object_name = 'song_list'

    def get_queryset(self):
        return Song.objects.select_related('songurl')


class CatalogueView(ListView):
    model = Song
    template_name = 'base/library.html' 
    context_object_name = 'song_list'

    def get_queryset(self):
        return Song.objects.select_related('songurl')


class SongDetailView(DetailView):
    model = Song
    template_name = 'base/song_detail.html'
    context_object_name = 'song'

    def get_queryset(self):
        return Song.objects.select_related('songurl', 'songattempt')
    

