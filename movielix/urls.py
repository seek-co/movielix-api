from django.urls import path
from .views import MovieListCreateView, MovieDetailView, TagListCreateView, TagDetailView, CollectionListCreateView

urlpatterns = [
    path("movies/", MovieListCreateView.as_view(), name="movie-list-create"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("collections/", CollectionListCreateView.as_view(), name="collection-list-create"),
    path("tags/", TagListCreateView.as_view(), name="tag-list-create"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag-detail"),
]
