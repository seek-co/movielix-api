from django.contrib import admin
from .models import Movie, Collection, Watchlist, MovieStatus, Favorite, Tag, MovieReview, Genre

# Register your models here

admin.site.register(Movie)
admin.site.register(Collection)
admin.site.register(Watchlist)
admin.site.register(MovieStatus)
admin.site.register(MovieReview)
admin.site.register(Favorite)
admin.site.register(Tag)
admin.site.register(Genre)
