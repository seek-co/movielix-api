from django.urls import path
from .views import (
    MovieListView,
    MovieDetailView,
    TagListView,
    TagDetailView,
    CollectionListView,
    CollectionDetailView,
    GenreListView,
    WatchlistView,
    WatchlistByCollectionView,
    WatchlistDetailView,
    MovieReviewListView,
    MovieReviewDetailView,
    FavoriteListView,
    FavoriteDetailView,
    SignUpView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("collections/", CollectionListView.as_view(), name="collection-list"),
    path("collections/<int:pk>/", CollectionDetailView.as_view(), name="collection-detail"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag-detail"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("watchlists/", WatchlistView.as_view(), name="watchlists"),
    path("collections/<int:collection_id>/watchlist/", WatchlistByCollectionView.as_view(), name="collection-watchlist"),
    path("collections/<int:collection_id>/movie/<int:movie_id>/", WatchlistDetailView.as_view(), name="collection-watchlist-movie"),
    path("movies/<int:movie_id>/reviews/", MovieReviewListView.as_view(), name="moive-review"),
    path("movies/<int:movie_id>/reviews/<int:review_id>/", MovieReviewDetailView.as_view(), name="movie-review-detail"),
    path("favorites/", FavoriteListView.as_view(), name="favorite-list"),
    path("favorites/<int:collection_id>/", FavoriteDetailView.as_view(), name="favorite-detail"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
