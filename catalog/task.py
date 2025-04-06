from celery import shared_task
import requests
from django.utils import timezone
import random
from .models import TrendingReview

@shared_task
def update_recent_movies():
    TrendingReview.objects.all().delete()

    today = timezone.now().date()
    thirty_days_ago = today - timezone.timedelta(days=30)

    api_key = '746380f35f478dc2fa82a6825e3d5446'
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_date.gte={thirty_days_ago}&primary_release_date.lte={today}'
    response = requests.get(url)

    if response.status_code == 200:
        movies = response.json()['results']
        for movie in movies:
            tmdb_id = movie['id']
            rating = random.randint(1, 5)
            TrendingReview.objects.create(tmdb_id=tmdb_id, rating=rating)