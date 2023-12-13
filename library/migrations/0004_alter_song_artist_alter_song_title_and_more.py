# Generated by Django 5.0 on 2023-12-13 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_songurl_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='songsearch',
            name='search_term',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='songurl',
            name='img_url',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='songurl',
            name='karaoke_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='songurl',
            name='lyric_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='songurl',
            name='mp3_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='songurl',
            name='tab_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
