from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tags_added")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["created_at"]


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name="collections", blank=True)
    is_public = models.BooleanField(default=False)
    url = models.CharField(max_length=500, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({'Public' if self.is_public else 'Private'})"
    
    class Meta:
        ordering = ["created_at"]

class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["created_at"]

class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview  = models.TextField(blank=True)
    release_year = models.PositiveIntegerField(blank=True, null=True)
    poster_url = models.CharField(max_length=500, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="movies_added")
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    duration = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}{f' ({self.release_year})' if self.release_year else ''}"

    class Meta:
        ordering = ["created_at"]


class Watchlist(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="wacthlists")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Watchlist for {self.collection.user.username} — Collection: '{self.collection.title}' — Movie: '{self.movie.title}'"
 

class MovieReview(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.username}"

    class Meta:
        ordering = ["created_at"]

class MovieStatus(models.Model):
    WATCH_STATUS_CHOICES = [
        ("want_to_watch", "Want to Watch"),
        ("watching", "Watching"),
        ("completed", "Completed"),
    ]

    watchlist = models.OneToOneField(Watchlist, on_delete=models.CASCADE, related_name="status")
    status = models.CharField(max_length=20, choices=WATCH_STATUS_CHOICES, default="want_to_watch")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    date_watched = models.DateField(null=True, blank=True)

    watch_location = models.CharField(max_length=100, blank=True, null=True)
    watched_with = models.CharField(max_length=100, blank=True, null=True)
    mood = models.CharField(max_length=100, blank=True, null=True)
    thoughts = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status_label = self.get_status_display()
        rating_status = f"Rating: {self.rating} stars" if self.rating else "No Rating"
        return f"{status_label} | {rating_status}"
    
    class Meta:
        ordering = ["created_at"]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "collection"], name="unique_user_collection_favorite")
        ]
        ordering = ["created_at"]
        
    def __str__(self):
        return f"{self.user.username} favorited Collection:{self.collection.title}"
