from django.db import models

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    artist = models.CharField(max_length=255, null=True)
    lyric = models.TextField(null=True)

    def __str__(self):
        return self.title


class SongUrl(models.Model):
    id = models.OneToOneField(Song, on_delete=models.CASCADE, primary_key=True)
    mp3 = models.CharField(max_length=255, null=True)
    karaoke = models.CharField(max_length=255, null=True)
    tab = models.CharField(max_length=255, null=True)
    img = models.TextField(null=True)

    def __str__(self):
        return self.id.title


class SongAttempt(models.Model):
    id = models.OneToOneField(Song, on_delete=models.CASCADE, primary_key=True)
    lyric = models.BooleanField(default=False)
    mp3 = models.BooleanField(default=False)
    karaoke = models.BooleanField(default=False)
    tab = models.BooleanField(default=False)

    def __str__(self):
        return self.id.title

class SongSearch(models.Model):
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE, null=True)
    search_term = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.song_id.title