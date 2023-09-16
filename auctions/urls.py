from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("filtercatagories", views.filtercatagories, name="filtercatagories"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),
]
