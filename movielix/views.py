from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Tag, Collection, Genre, Watchlist, MovieReview
from .serializers import MovieSerializer, TagSerializer, CollectionSerializer, GenreSerializer, WatchlistSerializer, MovieReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

# Create your views here.

class MovieListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MovieDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        return get_object_or_404(Movie, pk=pk)
    
    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        movie =self.get_object(pk)
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
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
    permission_classes = [AllowAny]
    
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
        tag.movies.clear()
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CollectionListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        movies = Collection.objects.all()
        serializer = CollectionSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CollectionDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get_object(self, pk):
        return get_object_or_404(Collection, pk=pk)
    
    def get(self, request, pk):
        collection = self.get_object(pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        collection = self.get_object(pk)
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        collection = self.get_object(pk)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GenreListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class WatchlistView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        watchlists = Watchlist.objects.all().select_related("movie", "collection")
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WatchlistByCollectionView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, collection_id):
        watchlist = Watchlist.objects.filter(collection_id=collection_id).select_related("movie")
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, collection_id):
        movie_id = request.data.get("movie_id")
        if not movie_id:
            return Response({"error": "movie_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if Watchlist.objects.filter(collection_id=collection_id, movie_id=movie_id).exists():
            return Response({"error": "Movie already in collection"}, status=status.HTTP_400_BAD_REQUEST)

        watchlist = Watchlist.objects.create(collection_id=collection_id, movie=movie)
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class WatchlistDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, collection_id, movie_id):
        watchlist = get_object_or_404(
            Watchlist.objects.select_related("movie", "collection"),
            collection_id=collection_id,
            movie_id=movie_id
        )
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, collection_id, movie_id):
        try:
            watchlist = Watchlist.objects.get(collection_id=collection_id, movie_id=movie_id)
            watchlist.delete()
            return Response({"message": "Movie removed from collection"}, status=status.HTTP_204_NO_CONTENT)
        except Watchlist.DoesNotExist:
            return Response({"error": "Movie not found in collection"}, status=status.HTTP_404_NOT_FOUND)
        
        
class MovieReviewListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        reviews = MovieReview.objects.filter(movie_id=movie_id).select_related("user")
        serializer = MovieReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        if MovieReview.objects.filter(movie_id=movie_id, user=request.data.get("user")).exists():
            return Response({"error": "You have already reviewed this movie."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MovieReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)