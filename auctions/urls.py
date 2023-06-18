from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("display_my_listings", views.display_my_listings, name="display_my_listings"),
    path("my_watchlist", views.display_watchlist, name="display_watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("close_listing<int:listing_id>", views.close_listing, name="close_listing"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("delete_listing/<int:listing_id>", views.delete_listing, name="delete_listing"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("login", views.login_view, name="login"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("modify_listing<int:listing_id>", views.modify_listing, name="modify_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name='category')
]
