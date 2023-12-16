from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .python_resources.all_music_scraper import AllMusicScraper

from library.models import Song, SongSearch, UserSong


class MyFormView(LoginRequiredMixin, View):
    template_name = 'base/find-song.html'

    def get(self, request):
        return render(request, self.template_name)


class SongSearchView(View):
    def post(self, request, song_title=None):
        song_search = SongSearch.objects.filter(search_term__iexact=song_title).first()

        if song_search:
            song = Song.objects.get(id=song_search.song_id_id)
            UserSong.objects.get_or_create(user=request.user, song=song)

            return JsonResponse({'song_id': song.id})
        else:
            return JsonResponse({'message': 'Not Found'})
        

class CorrectTitleArtist(View):
    def get(self, request):
        title = request.GET.get('title')
        artist = request.GET.get('artist')

        scraper = AllMusicScraper(title=title, artist=artist if artist else None)

        correct_title, correct_artist = scraper.run_scrape()
        correct_title = correct_title.strip()
        correct_artist = correct_artist.strip()

        song_search = SongSearch.objects.filter(search_term__iexact=correct_title).first()

        if song_search:
            SongSearch.objects.create(song_id=song_search.song_id, search_term=correct_title)
        else:
            song = Song.objects.create(title=correct_title, artist=correct_artist)
            UserSong.objects.create(user=request.user, song=song)
            SongSearch.objects.create(song_id=song, search_term=correct_title)
            if correct_title != title:
                SongSearch.objects.create(song_id=song, search_term=title)
           

        return JsonResponse({'status': 'success'})


    
