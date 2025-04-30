from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    url = models.CharField(max_length=22, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({'Public' if self.is_public else 'Private'})"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_year = models.PositiveIntegerField(blank=True, null=True)
    poster_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {f' - ({self.release_year})' if self.release_year else ''}"


class CollectionMovie(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collection_movies")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class MovieStatus(models.Model):
    collection_movie = models.OneToOneField(CollectionMovie, on_delete=models.CASCADE, related_name="status")
    watched = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    review = models.TextField(blank=True)

    def __str__(self):
        watched_status = "Watched" if self.watched else "Not Watched"
        rating_status = f"Rating: {self.rating}" if self.rating else "No Rating"
        review_status = f"Review: {self.review[:50]}..." if self.review else "No Review"
        
        return f"{watched_status} | {rating_status} | {review_status}"

WATCH_LOCATIONS = (
    ("c", "Cinema"),
    ("h", "Home"),
    ("o", "Other"),
)

WATCH_WITH = (
    ("a", "Alone"),
    ("r", "Friends Night"),
    ("m", "Family Night"),
    ("o", "Other"),
)


class Note(models.Model):
    collection_movie = models.OneToOneField("CollectionMovie", on_delete=models.CASCADE, related_name="note")
    watch_date = models.DateField(blank=True, null=True)
    watch_location = models.CharField(max_length=1, choices=WATCH_LOCATIONS, blank=True, null=True)
    watch_with = models.CharField(max_length=1, choices=WATCH_WITH, blank=True, null=True)

    def __str__(self):
        date_str = self.watch_date if self.watch_date else 'Unknown'
        location_str = self.get_watch_location_display() if self.watch_location else 'Unknown'
        with_str = self.get_watch_with_display() if self.watch_with else 'Unknown'
        
        return f"Watch date: {date_str}, Location: {location_str}, Watch with: {with_str}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "collection"], name="unique_user_collection_favorite")
        ]
