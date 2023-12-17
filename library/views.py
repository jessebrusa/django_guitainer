from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
import json

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
        return Song.objects.select_related('songurl', 'songattempt').prefetch_related('usersong_set')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_song = UserSong.objects.filter(user=self.request.user, song=self.object).first()
        context['is_in_library'] = user_song is not None
        context['is_favorite'] = user_song.favorite if user_song else False
        return context


class AddRemoveFavoritesView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        song_id = data.get('song_id', None)
        user_id = data.get('user_id', None)
        action = data.get('action', None)

        user_song = UserSong.objects.get(user_id=user_id, song_id=song_id)
        if action == 'add':
            user_song.favorite = True
        else:  
            user_song.favorite = False
        user_song.save()

        return JsonResponse({'is_favorite': user_song.favorite})