from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .python_resources.all_music_scraper import AllMusicScraper
from .python_resources.tab_scraper import TabScraper
from .python_resources.resources import *

from library.models import Song, SongSearch, UserSong, SongUrl, SongAttempt

import os
import asyncio
from dotenv import load_dotenv


load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')  
GENIUS_ACCESS_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN')


class MyFormView(LoginRequiredMixin, View):
    template_name = 'base/find-song.html'

    def get(self, request):
        return render(request, self.template_name)


class SongSearchView(View):
    def get(self, request):
        song_title = request.GET.get('song_title', None)
        if not song_title:
            return JsonResponse({'message': 'Missing song_title parameter'}, status=400)

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
            
            SongUrl.objects.create(id=song)
            SongAttempt.objects.create(id=song)

            song_id = song.id
           
        return JsonResponse({'status': 'success', 'song_id': song_id, 'correct_title': correct_title, 'correct_artist': correct_artist})
   

class ObtainImgView(View):
    def get(self, request, *args, **kwargs):
        song_id = request.GET.get('song_id', None)
        title = request.GET.get('title', None)
        artist = request.GET.get('artist', None)

        if artist:
            query = f"{title} {artist}"
        else:
            query = title

        img_url = get_google_img(query, GOOGLE_API_KEY, GOOGLE_CX)

        if img_url:
            song_url = SongUrl.objects.get(id=song_id)
            song_url.img = img_url
            song_url.save()

        return JsonResponse({'status': 'success'})
    

class ObtainLyricsView(View):
    def get(self, request, *args, **kwargs):
        song_id = request.GET.get('song_id', None)
        title = request.GET.get('title', None)
        artist = request.GET.get('artist', None)

        lyrics = obtain_Genius_lyrics(GENIUS_ACCESS_TOKEN, title, artist=artist)

        if lyrics is None:
            lyrics = obtain_AZ_lyrics(title, artist=artist)

        if lyrics:
            song = Song.objects.get(id=song_id)
            song.lyric = lyrics
            song.save()

            song_attempt = SongAttempt.objects.get(id=song_id)
            song_attempt.lyric = True
            song_attempt.save()

        return JsonResponse({'status': 'success'})
    

class ObtainMp3View(View):
    def get(self, request, *args, **kwargs):
        song_id = request.GET.get('song_id', None)
        title = request.GET.get('title', None)
        artist = request.GET.get('artist', None)

        mp3_url = download_and_upload_mp3(title, artist)

        if mp3_url:
            song_url = SongUrl.objects.get(id=song_id)
            song_url.mp3 = mp3_url
            song_url.save()

            song_attempt = SongAttempt.objects.get(id=song_id)
            song_attempt.mp3 = True
            song_attempt.save()

            return JsonResponse({'status': 'success'})

        else:
            return JsonResponse({'status': 'failure'})
        

class ObtainKaraokeView(View):
    def get(self, request, *args, **kwargs):
        song_id = request.GET.get('song_id', None)
        title = request.GET.get('title', None)

        karaoke_url = download_and_upload_karaoke(title)

        if karaoke_url:
            song_url = SongUrl.objects.get(id=song_id)
            song_url.karaoke = karaoke_url
            song_url.save()

            song_attempt = SongAttempt.objects.get(id=song_id)
            song_attempt.karaoke = True
            song_attempt.save()

            return JsonResponse({'status': 'success'})

        else:
            return JsonResponse({'status': 'failure'})
        

class ObtainTabView(View):
    def get(self, request, *args, **kwargs):
        song_id = request.GET.get('song_id', None)
        title = request.GET.get('title', None)


        scraper = TabScraper(title)
    
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            tab_href = loop.run_until_complete(scraper.run_scrape())
            tab_url = loop.run_until_complete(scraper.download_pdf(tab_href))
        finally:
            loop.close()
            
        if tab_url:
            song_url = SongUrl.objects.get(id=song_id)
            song_url.tab = tab_url
            song_url.save()

            song_attempt = SongAttempt.objects.get(id=song_id)
            song_attempt.tab = True
            song_attempt.save()

            return JsonResponse({'status': 'success'})
        
        else:
            return JsonResponse({'status': 'failure'})