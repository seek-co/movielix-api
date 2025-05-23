from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Movie,
    Tag,
    Collection,
    Genre,
    Watchlist,
    MovieReview,
    Favorite,
    MovieStatus,
)
from .serializers import (
    MovieSerializer,
    TagSerializer,
    CollectionSerializer,
    GenreSerializer,
    WatchlistSerializer,
    MovieReviewSerializer,
    FavoriteSerializer,
    CollectionCreateSerializer,
    MovieDetailSerializer,
    CollectionPatchSerializer,
    MovieStatusSerializer,
)
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count

# Create your views here.


class MovieListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_only = request.query_params.get("mine") == "true"
        if user_only:
            movies = Movie.objects.filter(added_by=request.user)
        else:
            movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Movie, pk=pk)

    def get(self, request, pk):
        movie = self.get_object(pk)
        user = request.user
        serializer = MovieDetailSerializer(movie, context={"user": user})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        movie = self.get_object(pk)
        if movie.added_by != request.user:
            return Response(
                {"error": "You do not have permission to edit this movie."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        if movie.added_by != request.user:
            return Response(
                {"error": "You do not have permission to delete this movie."},
                status=status.HTTP_403_FORBIDDEN,
            )
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Tag, pk=pk)

    def get(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tag = self.get_object(pk)
        tag.collections.clear()
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        collections = Collection.objects.filter(user=user)
        serializer = CollectionSerializer(
            collections, many=True, context={"user": user}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CollectionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Collection, pk=pk)

    def get(self, request, pk):
        user = request.user
        collection = self.get_object(pk)
        if collection.user != user and not collection.is_public:
            return Response(
                {"detail": "You do not have permission to view this collection."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CollectionSerializer(collection, context={"user": user})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        collection = self.get_object(pk)
        if collection.user != request.user:
            return Response(
                {"error": "You do not have permission to edit this collection."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CollectionPatchSerializer(
            collection, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        collection = self.get_object(pk)
        if collection.user != request.user:
            return Response(
                {"error": "You do not have permission to delete this collection."},
                status=status.HTTP_403_FORBIDDEN,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WatchlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        watchlists = Watchlist.objects.all().select_related("movie", "collection")
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WatchlistByCollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, collection_id):
        watchlist = Watchlist.objects.filter(
            collection_id=collection_id
        ).select_related("movie")
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, collection_id):
        movie_id = request.data.get("movie_id")
        if not movie_id:
            return Response(
                {"error": "movie_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        movie = get_object_or_404(Movie, id=movie_id)

        if Watchlist.objects.filter(
            collection_id=collection_id, movie_id=movie_id
        ).exists():
            return Response(
                {"error": "Movie already in collection"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        watchlist = Watchlist.objects.create(collection_id=collection_id, movie=movie)
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WatchlistDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, collection_id, movie_id):
        watchlist = get_object_or_404(
            Watchlist.objects.select_related("movie", "collection"),
            collection_id=collection_id,
            movie_id=movie_id,
        )
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, collection_id, movie_id):
        try:
            watchlist = Watchlist.objects.get(
                collection_id=collection_id, movie_id=movie_id
            )
            watchlist.delete()
            return Response(
                {"message": "Movie removed from collection"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Watchlist.DoesNotExist:
            return Response(
                {"error": "Movie not found in collection"},
                status=status.HTTP_404_NOT_FOUND,
            )


class MovieReviewListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        reviews = MovieReview.objects.filter(movie_id=movie_id).select_related("user")
        serializer = MovieReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        user_id = request.data.get("user")
        if not user_id:
            return Response(
                {"error": "user is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if MovieReview.objects.filter(movie_id=movie_id, user=user_id).exists():
            return Response(
                {"error": "You have already reviewed this movie."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = MovieReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, review_id):
        review = get_object_or_404(MovieReview, id=review_id, movie_id=movie_id)
        serializer = MovieReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, movie_id, review_id):
        review = get_object_or_404(MovieReview, id=review_id, movie_id=movie_id)
        serializer = MovieReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id, review_id):
        review = get_object_or_404(MovieReview, id=review_id, movie_id=movie_id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(
            favorites, many=True, context={"user": request.user}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        collection_id = request.data.get("collection")

        if not collection_id:
            return Response(
                {"detail": "Collection ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        collection = get_object_or_404(Collection, id=collection_id)

        if collection.user != user and not collection.is_public:
            return Response(
                {"detail": "You cannot favorite this private collection."},
                status=status.HTTP_403_FORBIDDEN,
            )

        favorite, created = Favorite.objects.get_or_create(
            user=user, collection=collection
        )

        if created:
            return Response(
                {"message": "Added to favorites"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "Already in favorites"}, status=status.HTTP_200_OK
            )


class FavoriteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, collection_id):
        user = request.user
        favorite = get_object_or_404(Favorite, user=user, collection__id=collection_id)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, collection_id):
        user = request.user
        favorite = get_object_or_404(Favorite, user=user, collection__id=collection_id)
        favorite.delete()
        return Response(
            {"detail": "Favorite removed."}, status=status.HTTP_204_NO_CONTENT
        )


class WatchlistMovieStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, watchlist_id, movie_id):
        watchlist = get_object_or_404(
            Watchlist, 
            id=watchlist_id,
            collection__user=request.user,
            movie__id=movie_id
        )

        serializer = WatchlistSerializer(watchlist)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PublicCollectionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        collections = Collection.objects.filter(is_public=True)
        serializer = CollectionSerializer(
            collections, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)



class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username", "").strip()
        email = request.data.get("email", "").strip()
        password = request.data.get("password", "").strip()

        if not all([username, email, password]):
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password)
        except ValidationError as error:
            return Response(
                {"error": error.messages}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        tokens = RefreshToken.for_user(user)
        return Response(
            {"refresh": str(tokens), "access": str(tokens.access_token)},
            status=status.HTTP_201_CREATED,
        )
