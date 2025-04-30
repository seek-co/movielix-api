from django.contrib import admin
from .models import Movie, Collection, Watchlist, MovieStatus, Favorite, Tag

# Register your models here

admin.site.register(Movie)
admin.site.register(Collection)
admin.site.register(Watchlist)
admin.site.register(MovieStatus)
admin.site.register(Favorite)
admin.site.register(Tag)

