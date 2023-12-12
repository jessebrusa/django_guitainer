from django.db import models

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class SongUrl(models.Model):
    id = models.OneToOneField(Song, on_delete=models.CASCADE, primary_key=True)
    lyric_url = models.CharField(max_length=255)
    mp3_url = models.CharField(max_length=255)
    karaoke_url = models.CharField(max_length=255)
    tab_url = models.CharField(max_length=255)
    img_url = models.TextField()

    def __str__(self):
        return self.id.title


class SongAttempt(models.Model):
    id = models.OneToOneField(Song, on_delete=models.CASCADE, primary_key=True)
    lyric = models.BooleanField(default=False)
    mp3 = models.BooleanField(default=False)
    karaoke = models.BooleanField(default=False)
    tab = models.BooleanField(default=False)
    img = models.BooleanField(default=False)

    def __str__(self):
        return self.id.title

class SongSearch(models.Model):
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE, null=True)
    search_term = models.CharField(max_length=255)

    def __str__(self):
        return self.song_id.title