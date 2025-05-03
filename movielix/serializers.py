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
    is_favorite = serializers.SerializerMethodField()
    class Meta:
        model = Collection
        fields = '__all__'
        
    def get_is_favorite(self, obj):
        user = self.context.get('user')
        if user and not user.is_anonymous:
            return obj.favorites.filter(user=user).exists()
        return False
        
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
    collection = CollectionSerializer()

    class Meta:
        model = Favorite
        fields = '__all__'