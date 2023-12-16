import requests
import azapi
from lyricsgenius import Genius
import re
import os


def download_song(title, artist, path):
    query = f"{title} {artist} audio"
    try:
        videos_search = VideosSearch(query, limit=1)
        video_url = videos_search.result()['result'][0]['link']
        
        os.environ['SSL_CERT_FILE'] = certifi.where()

        youtube = YouTube(video_url)
        audio_stream = youtube.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=path, filename=f'{title}.mp3')

        return True
    
    except:
        return False


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