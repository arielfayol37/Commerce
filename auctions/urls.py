from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_watchlist", views.display_watchlist, name="display_watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
