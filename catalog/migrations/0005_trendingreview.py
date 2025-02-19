# Generated by Django 5.1.5 on 2025-02-07 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_review_book_remove_review_movie_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrendingReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmdb_id', models.IntegerField()),
                ('rating', models.IntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
