# Generated by Django 5.0 on 2023-12-12 21:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songattempt',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='library.song'),
        ),
        migrations.AlterField(
            model_name='songsearch',
            name='song_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='library.song'),
        ),
    ]
