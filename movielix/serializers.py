from rest_framework import serializers
from .models import Movie, Tag, Collection, Genre, Watchlist, MovieReview, Favorite

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    collection_title = serializers.CharField(source="collection.title", read_only=True)
    class Meta:
        model = Watchlist
        fields = ["id", "collection", "collection_title", "movie", "movie_title", "created_at", "updated_at"]

class MovieReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = MovieReview
        fields = ["id", "user", "username", "rating", "review", "movie", "created_at", "updated_at"]
        read_only_fields = ["movie", "username", "created_at", "updated_at"]


class FavoriteSerializer(serializers.ModelSerializer):
    collection_title = serializers.CharField(source="collection.title", read_only=True)
    collection_owner = serializers.CharField(source="collection.user.username", read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "collection", "collection_title", "collection_owner", "created_at", "updated_at"]