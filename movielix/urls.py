from django.urls import path
from .views import MovieListView, MovieDetailView, TagListView, TagDetailView, CollectionListView, CollectionDetailView, GenreListView, WatchlistView, WatchlistByCollectionView, WatchlistDetailView

urlpatterns = [
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("collections/", CollectionListView.as_view(), name="collection-list"),
    path("collections/<int:pk>/", CollectionDetailView.as_view(), name="collection-detail"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag-detail"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("watchlists/", WatchlistView.as_view()),
    path("collections/<int:collection_id>/watchlist/", WatchlistByCollectionView.as_view()),
    path("collections/<int:collection_id>/movie/<int:movie_id>/", WatchlistDetailView.as_view())
]
