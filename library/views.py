from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Song, UserSong


class LibraryView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'base/library.html' 
    context_object_name = 'song_list'

    def get_queryset(self):
        return Song.objects.select_related('songurl').filter(usersong__user=self.request.user)


class CatalogueView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'base/catalogue.html' 
    context_object_name = 'song_list'

    def get_queryset(self):
        return Song.objects.select_related('songurl').exclude(usersong__user=self.request.user)


class AddToLibraryView(LoginRequiredMixin, View):
    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        UserSong.objects.create(user=request.user, song=song)
        return JsonResponse({'status': 'success'})
    

class RemoveFromLibraryView(LoginRequiredMixin, View):
    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        UserSong.objects.filter(user=request.user, song=song).delete()
        return JsonResponse({'status': 'success'})


class SongDetailView(LoginRequiredMixin, DetailView):
    model = Song
    template_name = 'base/song_detail.html'
    context_object_name = 'song'

    def get_queryset(self):
        return Song.objects.select_related('songurl', 'songattempt')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_in_library'] = UserSong.objects.filter(user=self.request.user, song=self.object).exists()
        return context
    

