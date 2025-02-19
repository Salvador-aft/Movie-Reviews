from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import random
from .models import TrendingReview 

class RecentMovies(APIView):
    def get(self, request):
        today = timezone.now().date()
        thirty_days_ago = today - timezone.timedelta(days=30)

        api_key = '746380f35f478dc2fa82a6825e3d5446'
        url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_date.gte={thirty_days_ago}&primary_release_date.lte={today}'
        response = requests.get(url)

        if response.status_code == 200:
            movies = response.json()['results']

            if len(movies) < 5:
                remaining = 5 - len(movies)
                older_movies_url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_date.lte={thirty_days_ago}&sort_by=release_date.desc'
                older_movies_response = requests.get(older_movies_url)

                if older_movies_response.status_code == 200:
                    older_movies = older_movies_response.json()['results'][:remaining]
                    movies.extend(older_movies)

            for movie in movies:
                tmdb_id = movie['id']
                rating = random.randint(1, 5)  # Reseña aleatoria entre 1 y 5
                TrendingReview.objects.create(tmdb_id=tmdb_id, rating=rating)

            reviews = TrendingReview.objects.filter(created_at__gte=thirty_days_ago)
            review_data = [{'tmdb_id': review.tmdb_id, 'rating': review.rating} for review in reviews]
            return Response(review_data)
        else:
            return Response({'error': 'No se pudieron obtener las películas'}, status=500)
        
class TopRatedMovies(APIView):
    def get(self, request):
        top_reviews = TrendingReview.objects.filter(rating=5).order_by('-rating')[:5]

        if len(top_reviews) < 5:
            remaining = 5 - len(top_reviews)
            next_reviews = TrendingReview.objects.filter(rating__lt=5).order_by('-rating')[:remaining]
            top_reviews = list(top_reviews) + list(next_reviews)

        tmdb_ids = [review.tmdb_id for review in top_reviews]

        api_key = '746380f35f478dc2fa82a6825e3d5446'
        movie_data = []

        for tmdb_id in tmdb_ids:
            movie_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}'
            movie_response = requests.get(movie_url)

            if movie_response.status_code == 200:
                movie_info = movie_response.json()

                poster_path = movie_info.get('poster_path')
                poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}' if poster_path else None

                videos_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}/videos?api_key={api_key}'
                videos_response = requests.get(videos_url)
                trailer_url = None

                if videos_response.status_code == 200:
                    videos_info = videos_response.json()
                    for video in videos_info.get('results', []):
                        if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
                            trailer_url = f'https://www.youtube.com/watch?v={video.get("key")}'
                            break

                movie_data.append({
                    'title': movie_info.get('title'),
                    'genre': ', '.join([genre['name'] for genre in movie_info.get('genres', [])]),
                    'duration': movie_info.get('runtime'),
                    'release_date': movie_info.get('release_date'),
                    'is_upcoming': False,
                    'rating': next(review.rating for review in top_reviews if review.tmdb_id == tmdb_id),
                    'poster_url': poster_url, 
                    'trailer_url': trailer_url,
                    'overview': movie_info.get('overview', 'Sin sinopsis disponible'),
                })
            else:
                movie_data.append({
                    'title': 'Película no disponible',
                    'genre': 'N/A',
                    'duration': 0,
                    'release_date': 'N/A',
                    'is_upcoming': False,
                    'rating': 0,
                    'poster_url': None,
                    'trailer_url': None,
                    'overview': 'Sin sinopsis disponible',
                })

        return Response(movie_data)