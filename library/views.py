from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .forms import SongForm
import json

from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models import Q

from .models import Song, UserSong, SongUrl, SongAttempt   

import os
from google.cloud import storage
import tempfile


class LibraryView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'base/library.html' 
    context_object_name = 'song_list'

    def get_queryset(self):
        queryset = Song.objects.select_related('songurl').filter(Q(created=self.request.user) | Q(usersong__user=self.request.user))
        search_query = self.request.GET.get('search', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        queryset = queryset.order_by('title')  # order by title in ascending order
        return queryset

class CatalogueView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'base/catalogue.html' 
    context_object_name = 'song_list'

    def get_queryset(self):
        user_songs = UserSong.objects.filter(user=self.request.user).values_list('song', flat=True)
        queryset = Song.objects.select_related('songurl').exclude(created__isnull=False).exclude(id__in=user_songs)
        search_query = self.request.GET.get('search', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        queryset = queryset.order_by('title')  # order by title in ascending order
        return queryset
    

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
    template_name = 'base/song-detail.html'
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
    

class CreateGuitainerView(LoginRequiredMixin, View):
    def get(self, request):
        form = SongForm()
        return render(request, 'base/create-guitainer.html', {'form': form})

    def post(self, request):
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            new_song = Song()
            new_song.title = form.cleaned_data.get('title')
            url_title = new_song.title.replace(' ', '-')

            if form.cleaned_data.get('artist'):
                new_song.artist = form.cleaned_data.get('artist')


            new_song.created = request.user
            new_song.save()

            song_url = SongUrl(id=new_song)
            song_attempt = SongAttempt(id=new_song)


            if form.cleaned_data.get('lyric'):  
                new_song.lyric = form.cleaned_data.get('lyric')
                new_song.save()

                song_attempt.lyric = True
                song_attempt.save()


            if 'img_address' in request.POST:
                img_address = request.POST['img_address']
                
                song_url.img = img_address
                song_url.save()


            if 'karaoke' in request.FILES:
                karaoke_file = request.FILES['karaoke']
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                    for chunk in karaoke_file.chunks():
                        temp_file.write(chunk)

                client = storage.Client()
                bucket = client.get_bucket('guitainer')
                blob = bucket.blob(f'karaoke/{url_title}.mp4')
                blob.upload_from_filename(temp_file.name)
                os.remove(temp_file.name)

                song_url.karaoke = blob.public_url
                song_url.save()

                song_attempt.karaoke = True
                song_attempt.save()


            if 'mp3' in request.FILES:
                mp3_file = request.FILES['mp3']
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                    for chunk in mp3_file.chunks():
                        temp_file.write(chunk)

                client = storage.Client()
                bucket = client.get_bucket('guitainer')
                blob = bucket.blob(f'mp3/{url_title}.mp3')
                blob.upload_from_filename(temp_file.name)
                os.remove(temp_file.name)

                song_url.mp3 = blob.public_url
                song_url.save()

                song_attempt.mp3 = True
                song_attempt.save()


            if 'tabs' in request.FILES:
                tabs_file = request.FILES['tabs']
                tabs_path = os.path.join(settings.MEDIA_ROOT, 'tab', f"{url_title}.pdf")
                with open(tabs_path, 'wb+') as destination:
                    for chunk in tabs_file.chunks():
                        destination.write(chunk)

                db_tabs_path = f'/media/tab/{url_title}.pdf'
                song_url.tab = db_tabs_path
                song_url.save()

                song_attempt.tab = True
                song_attempt.save()


            return redirect('/song/' + str(new_song.id))
        return render(request, 'base/create-guitainer.html', {'form': form})