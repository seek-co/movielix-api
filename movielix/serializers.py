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
        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    class Meta:
        model = Watchlist
        fields = ["id", "collection", "movie", "created_at", "updated_at"]

class MovieReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = MovieReview
        fields = ["id", "user", "username", "rating", "review", "movie", "created_at", "updated_at"]
        read_only_fields = ["movie", "username", "created_at", "updated_at"]
        
class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'tags', 'is_public', 'url']

class CollectionSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    movie_count = serializers.SerializerMethodField()
    username = serializers.CharField(source="user.username", read_only=True)
    is_mine = serializers.SerializerMethodField()
    watchlists = WatchlistSerializer(many=True)
    tags = TagSerializer(many=True)
        
    class Meta:
        model = Collection
        fields = '__all__'
        
    def get_is_favorite(self, obj):
        user = self.context.get("user")
        if user and not user.is_anonymous:
            return obj.favorites.filter(user=user).exists()
        return False
    
    def get_movie_count(self, obj):
        return obj.watchlists.count()
    
    def get_is_mine(self, obj):
        user = self.context.get("user")
        return user == obj.user if user and not user.is_anonymous else False

class FavoriteSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer()

    class Meta:
        model = Favorite
        fields = '__all__'
        