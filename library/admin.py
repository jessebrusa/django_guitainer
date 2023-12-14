from django.contrib import admin
from .models import Song, SongUrl, SongAttempt, SongSearch, UserSong

admin.site.register(Song)
admin.site.register(SongUrl)
admin.site.register(SongAttempt)
admin.site.register(SongSearch)
admin.site.register(UserSong)