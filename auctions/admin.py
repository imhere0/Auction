from django.contrib import admin
from .models import  Listing, Winner, Bid, Watchlist, Comment

# Register your models here.

admin.site.register(Listing)
admin.site.register(Winner)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Comment)