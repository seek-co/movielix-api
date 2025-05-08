from rest_framework import serializers
from .models import Movie, Tag, Collection, Genre, Watchlist, MovieReview, Favorite, MovieStatus


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class MovieStatusSerializer(serializers.ModelSerializer):
    movie_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)


    class Meta:
        model = MovieStatus
        fields = '__all__'

    def get_movie_id(self, obj):
        return obj.watchlist.movie.id

    def get_user_id(self, obj):
        return obj.watchlist.collection.user.id

class MovieDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="added_by.username", read_only=True)
    is_mine = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = "__all__"

    def get_is_mine(self, obj):
        user = self.context.get("user")
        return user == obj.added_by if user and not user.is_anonymous else False


class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    status = MovieStatusSerializer()

    class Meta:
        model = Watchlist
        fields = ["id", "collection", "movie", "status", "created_at", "updated_at"]


class MovieReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = MovieReview
        fields = [
            "id",
            "user",
            "username",
            "rating",
            "review",
            "movie",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["movie", "username", "created_at", "updated_at"]


class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["title", "description", "tags", "is_public", "url"]


class CollectionPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "description", "tags", "is_public", "url"]


class CollectionSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    movie_count = serializers.SerializerMethodField()
    username = serializers.CharField(source="user.username", read_only=True)
    is_mine = serializers.SerializerMethodField()
    watchlists = WatchlistSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Collection
        fields = "__all__"

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
        fields = "__all__"
