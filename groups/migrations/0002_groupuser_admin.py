# Generated by Django 5.0 on 2023-12-17 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupuser',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
