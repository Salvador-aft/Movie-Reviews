from django.urls import path
from .views import RecentMovies
from .views import RecentMovies, TopRatedMovies

urlpatterns = [
    path('recent-movies/', RecentMovies.as_view(), name='recent-movies'),
    path('top-rated-movies/', TopRatedMovies.as_view(), name='top-rated-movies'),
]