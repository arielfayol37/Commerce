from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ListingForm


def index(request):
    # listings_html = [listing.html() for listing in Listing.objects.all()]
    listings= [listing for listing in Listing.objects.all()]
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            try:
                category = Category.objects.get(name=form.cleaned_data['category'])
            except Category.DoesNotExist:
                category = Category.objects.create(name=form.cleaned_data['category'])
            listing.category = category
            listing.save()
            messages.success(request, 'Listing created successfully.')
            return redirect('listing', listing_id=listing.id)
        else:
            messages.error(request, 'There was an error with your submission.')
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {'form': form})

def listing(request, listing_id):
    item = Listing.objects.get(pk = listing_id)
    return render(request, "auctions/listing.html", {"listing": item})

@login_required
def watchlist(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    wlistings = request.user.watchlist.all()
    if listing in wlistings:
        request.user.watchlist.remove(listing)
        
    else:
        request.user.watchlist.add(listing)
    # return redirect('listing', listing_id=listing.id)
    return redirect('display_watchlist')

@login_required
def display_watchlist(request):
    wlistings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"wlistings": wlistings})