# Generated by Django 5.1.5 on 2025-02-06 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_movie_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='book',
        ),
        migrations.RemoveField(
            model_name='review',
            name='movie',
        ),
        migrations.AddField(
            model_name='review',
            name='tmdb_id',
            field=models.IntegerField(default=0),
        ),
    ]
