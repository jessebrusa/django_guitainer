# Generated by Django 5.0 on 2023-12-13 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_remove_songurl_lyric_url_song_lyrics'),
    ]

    operations = [
        migrations.RenameField(
            model_name='songurl',
            old_name='img_url',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='songurl',
            old_name='karaoke_url',
            new_name='karaoke',
        ),
        migrations.RenameField(
            model_name='songurl',
            old_name='mp3_url',
            new_name='mp3',
        ),
        migrations.RenameField(
            model_name='songurl',
            old_name='tab_url',
            new_name='tab',
        ),
        migrations.RemoveField(
            model_name='songattempt',
            name='img',
        ),
    ]
