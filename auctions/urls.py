from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name = "createListing"),
    path("closedlisting", views.closedListing, name = "closedListing"),
    path("categories",views.categories, name = "categories"),
    path("<str:id>", views.title, name = "title"),
    path("<str:username>/watchlist", views.watchlist, name = "watchlist"),
    path("<str:id>/remove", views.remove, name = "remove"),
    path("<str:category>/activelisting",views.categoricalactivelisting, name = "categoricalactivelisting")
]
