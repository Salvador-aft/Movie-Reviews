import os
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import random
from django.conf import settings
from .models import TrendingReview
from dotenv import load_dotenv

load_dotenv()

class RecentMovies(APIView):
    def get(self, request):
        try:
            today = timezone.now().date()
            thirty_days_ago = today - timezone.timedelta(days=30)
            
            api_key = os.getenv('TMDB_API_KEY')
            access_token = os.getenv('TMDB_ACCESS_TOKEN')
            
            if not api_key or not access_token:
                raise ValueError("Missing TMDB credentials in .env file")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "accept": "application/json"
            }
            
            url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_date.gte={thirty_days_ago}&primary_release_date.lte={today}'
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            movies = response.json().get('results', [])
            

            if len(movies) < 5:
                older_url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_date.lte={thirty_days_ago}&sort_by=release_date.desc'
                older_response = requests.get(older_url, headers=headers)
                older_response.raise_for_status()
                
                movies.extend(older_response.json().get('results', [])[:5 - len(movies)])
            
            for movie in movies[:10]:
                TrendingReview.objects.update_or_create(
                    tmdb_id=movie.get('id'),
                    defaults={
                        'rating': random.randint(1, 5),
                        'title': movie.get('title', 'Unknown')
                    }
                )
            
            reviews = TrendingReview.objects.filter(created_at__gte=thirty_days_ago).order_by('-created_at')[:10]
            return Response([
                {
                    'tmdb_id': r.tmdb_id,
                    'rating': r.rating,
                    'title': r.title
                } for r in reviews
            ])
            
        except requests.exceptions.RequestException as e:
            return Response({'error': f"TMDB API Error: {str(e)}"}, status=500)
        except Exception as e:
            return Response({'error': f"Server Error: {str(e)}"}, status=500)


class TopRatedMovies(APIView):
    def get(self, request):
        try:
            api_key = os.getenv('TMDB_API_KEY')
            access_token = os.getenv('TMDB_ACCESS_TOKEN')
            
            if not api_key or not access_token:
                raise ValueError("Missing TMDB credentials in .env file")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "accept": "application/json"
            }
            
            if TrendingReview.objects.exists():
                top_reviews = TrendingReview.objects.order_by('-rating')[:5]
            else:
                url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}'
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                for movie in response.json().get('results', [])[:5]:
                    release_date_str = movie.get('release_date')
                    try:
                        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date() if release_date_str else None
                    except:
                        release_date = None

                    review, created = TrendingReview.objects.get_or_create(
                        tmdb_id=movie['id'],
                        defaults={
                            'title': movie.get('title', 'Unknown'),
                            'rating': round(movie.get('vote_average', 5)),
                            'overview': movie.get('overview', ''),
                            'release_date': release_date,
                            'poster_path': movie.get('poster_path', ''),
                            'genres': ', '.join([str(g) for g in movie.get('genre_ids', [])]),
                            'duration': movie.get('runtime')
                        }
                    )
                
                top_reviews = TrendingReview.objects.order_by('-rating')[:5]
            
            movie_data = []
            for review in top_reviews:
                try:
                    movie_url = f'https://api.themoviedb.org/3/movie/{review.tmdb_id}?api_key={api_key}'
                    movie_response = requests.get(movie_url, headers=headers)
                    movie_response.raise_for_status()
                    movie_info = movie_response.json()
                    
                    trailer_url = None
                    videos_url = f'https://api.themoviedb.org/3/movie/{review.tmdb_id}/videos?api_key={api_key}'
                    videos_response = requests.get(videos_url, headers=headers)
                    
                    if videos_response.status_code == 200:
                        for video in videos_response.json().get('results', []):
                            if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
                                trailer_url = f'https://www.youtube.com/watch?v={video["key"]}'
                                break
                    
                    release_date_str = movie_info.get('release_date')
                    release_date = release_date_str if release_date_str else 'N/A'
                    
                    duration_min = movie_info.get('runtime')
                    if duration_min:
                        duration = f"{duration_min//60}h {duration_min%60}m"
                    else:
                        duration = 'N/A'
                    
                    movie_data.append({
                        'title': movie_info.get('title', review.title),
                        'genre': ', '.join([g['name'] for g in movie_info.get('genres', [])]) or 'N/A',
                        'duration': duration,
                        'release_date': release_date,
                        'is_upcoming': False,
                        'rating': review.rating,
                        'poster_url': f'https://image.tmdb.org/t/p/w500{movie_info["poster_path"]}' if movie_info.get('poster_path') else None,
                        'trailer_url': trailer_url,
                        'overview': movie_info.get('overview', 'Sin sinopsis disponible')
                    })
                    
                except requests.exceptions.RequestException:
                    release_date = review.release_date.strftime('%Y-%m-%d') if review.release_date else 'N/A'
                    
                    if review.duration:
                        duration = f"{review.duration//60}h {review.duration%60}m"
                    else:
                        duration = 'N/A'
                    
                    movie_data.append({
                        'title': review.title,
                        'genre': review.genres or 'N/A',
                        'duration': duration,
                        'release_date': release_date,
                        'is_upcoming': False,
                        'rating': review.rating,
                        'poster_url': f'https://image.tmdb.org/t/p/w500{review.poster_path}' if review.poster_path else None,
                        'trailer_url': None,
                        'overview': review.overview or 'Sin sinopsis disponible'
                    })
                    
            return Response(movie_data)
            
        except Exception as e:
            print(f">>> Error en TopRatedMovies: {str(e)}")
            return Response({'error': f"Server Error: {str(e)}"}, status=500)