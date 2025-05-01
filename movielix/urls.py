from django.urls import path
from .views import MovieListCreateView, TagListCreateView, TagDetailView

urlpatterns = [
    path("movies/", MovieListCreateView.as_view(), name="movie-list-create"),
    path("tags/", TagListCreateView.as_view(), name="tag-list-create"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag-detail"),
]
