from django.urls import path
from .views import MovieListCreateView, MovieDetailView, TagListCreateView, TagDetailView, CollectionListCreateView, CollectionDetailView, GenreListView

urlpatterns = [
    path("movies/", MovieListCreateView.as_view(), name="movie-list-create"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("collections/", CollectionListCreateView.as_view(), name="collection-list-create"),
    path("collections/<int:pk>/", CollectionDetailView.as_view(), name="collection-detail"),
    path("tags/", TagListCreateView.as_view(), name="tag-list-create"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag-detail"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
]
