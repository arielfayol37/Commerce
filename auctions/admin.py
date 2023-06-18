from django.contrib import admin

# Register your models here.
from .models import Category, Listing, User, Bid, Comment

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)