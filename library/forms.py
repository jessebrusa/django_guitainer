from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    img_address = forms.CharField(widget=forms.Textarea, required=False)
    mp3 = forms.FileField(required=False)
    karaoke = forms.FileField(required=False)
    tabs = forms.FileField(required=False)
    artist = forms.CharField(required=False)
    lyric = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Song
        fields = ['title', 'artist', 'lyric']