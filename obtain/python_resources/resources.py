from youtubesearchpython import VideosSearch
from pytube import YouTube
import requests
import azapi
from lyricsgenius import Genius
import re
import os
import certifi
from google.cloud import storage
import tempfile
from dotenv import load_dotenv

load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def download_and_upload_karaoke(title):
    query = f"{title} karaoke"

    videos_search = VideosSearch(query, limit=1)
    video_url = videos_search.result()['result'][0]['link']
    
    os.environ['SSL_CERT_FILE'] = certifi.where()

    youtube = YouTube(video_url)
    video_stream = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        video_stream.download(output_path=os.path.dirname(temp_file.name), filename=os.path.basename(temp_file.name))

    client = storage.Client()

    bucket = client.get_bucket('guitainer')

    blob = bucket.blob(f'karaoke/{title}.mp4')
    blob.upload_from_filename(temp_file.name)

    os.remove(temp_file.name)

    return blob.public_url


def download_and_upload_mp3(title, artist):
    query = f"{title} {artist} audio"

    videos_search = VideosSearch(query, limit=1)
    video_url = videos_search.result()['result'][0]['link']
    
    os.environ['SSL_CERT_FILE'] = certifi.where()

    youtube = YouTube(video_url)
    audio_stream = youtube.streams.filter(only_audio=True).first()

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        audio_stream.download(output_path=os.path.dirname(temp_file.name), filename=os.path.basename(temp_file.name))

    client = storage.Client()

    bucket = client.get_bucket('guitainer')

    blob = bucket.blob(f'mp3/{title}.mp3')
    blob.upload_from_filename(temp_file.name)

    os.remove(temp_file.name)


    return blob.public_url


def get_google_img(query, api_key, cx):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "searchType": "image"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if "items" in data and len(data["items"]) > 0:
            img_url = data["items"][0]["link"]
            return img_url

    return None


def obtain_AZ_lyrics(title, **kwargs):
    artist = kwargs.get('artist')
    API = azapi.AZlyrics('google', accuracy=0.5)
    API.title = title
    if artist:
        API.artist = artist

    API.getLyrics(save=False)
    if API.lyrics:
        return API.lyrics
    else:
        return None
    

def obtain_clean_lyrics(lyrics):
    metadata_patterns = [
        r"\[.*?\]", 
        r"\(.*?\)",  
        r"\d+\s*Contributors",  
        r"[\w\s]+ Lyrics",  
    ]


    exclude_patterns = [
        r"\d+Embed",  
    ]

    all_patterns = metadata_patterns + exclude_patterns
    all_regex = "|".join(all_patterns)

    cleaned_lyrics = re.sub(f".*?{all_regex}|{all_regex}.*?$", "", lyrics)

    return cleaned_lyrics.strip()


def obtain_Genius_lyrics(token, title, **kwargs):
    artist = kwargs.get('artist')

    genius = Genius(token)

    if artist:
        song = genius.search_song(title, artist)
    else:
        song = genius.search_song(title)

    if song:
        lyrics = obtain_clean_lyrics(song.lyrics)

        return lyrics
    else:
        return None