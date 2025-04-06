from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save

class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('sci_fi', 'Science Fiction'),
        ('comedy', 'Comedy'),
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
    ]

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    duration = models.IntegerField(null=True, blank=True)
    release_date = models.DateField()
    tmdb_rating = models.FloatField(default=0)
    is_upcoming = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return self.title


class Book(models.Model):
    GENRE_CHOICES = [
        ('adventure', 'Adventure'),
        ('sci_fi', 'Science Fiction'),
        ('police', 'Police'),
        ('horror', 'Horror and Suspense'),
        ('romance', 'Romance'),
    ]

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    pages = models.IntegerField()
    release_date = models.DateField()
    is_upcoming = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    tmdb_id = models.IntegerField(default=0)
    rating = models.IntegerField(choices=[(i, f'{i} star{"s" if i > 1 else ""}') for i in range(1, 6)])

    def __str__(self):
        return f"Review by {self.user.username} on movie ID {self.tmdb_id}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(
        default='http://localhost:5173/src/assets/profile-photo-default.jpg'
    )

    def __str__(self):
        return f"Profile of {self.user.username}"
    
class TrendingReview(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(choices=[(i, f'{i} star{"s" if i > 1 else ""}') for i in range(1, 6)])
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ['-rating']
        verbose_name_plural = "Trending Reviews"

    def __str__(self):
        return f"{self.title} ({self.rating} stars)" if self.title else f"Movie ID: {self.tmdb_id} ({self.rating} stars)"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()