from django.contrib.auth.models import User
from django.db import models
from library.models import Song


class Group(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name
    

class GroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    accept = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} in {self.group.name}'
    

class GroupSong(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.song.title} in {self.group.name}'