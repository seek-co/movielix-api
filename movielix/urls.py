from django.urls import path
from .views import MovieListCreateView, TagListCreateView

urlpatterns = [
    path("movies/", MovieListCreateView.as_view(), name="movie-list-create"),
    path("tags/", TagListCreateView.as_view(), name="tag-list-create"),
]
