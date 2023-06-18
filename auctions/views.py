from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ListingForm, BidForm


def index(request):
    # listings_html = [listing.html() for listing in Listing.objects.all()]
    listings= [listing for listing in Listing.objects.all()][::-1]
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
            cate = form.cleaned_data['category']
            if cate:
                try:
                    category = Category.objects.get(name=cate)
                except Category.DoesNotExist:
                    category = Category.objects.create(name=cate)
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
    user_is_winner = request.user == item.winner
    context = {"listing": item,
               "message": "",
               "user_is_winner": user_is_winner,
               "bidding_form": BidForm()
    }

    return render(request, "auctions/listing.html", context)

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
    wlistings = request.user.watchlist.all()[::-1]
    return render(request, "auctions/watchlist.html", {"wlistings": wlistings})

@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        content = request.POST['content']
        user = request.user
        listing = Listing.objects.get(pk=listing_id)

        comment = Comment(content=content, user=user, listing=listing)
        comment.save()

        return redirect('listing', listing_id=listing_id)
@login_required
def delete_listing(request, listing_id):
    listing = Listing.objects.get(pk =listing_id)
    listing.delete()
    return redirect('display_my_listings')

@login_required
def display_my_listings(request):
    my_listings = request.user.owned_listings.all()
    return render(request, "auctions/my_listings.html", {"my_listings":my_listings})
@login_required
def bid(request, listing_id):
    message = ""
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            listing = Listing.objects.get(pk = listing_id)
            if bid.price >= listing.current_price(): # updates the current price from previous bid
                bid.user = request.user
                bid.listing = listing
                bid.save()
                message = 'Bid Placed'
                messages.success(request, 'Bid Placed.')
                #return redirect('listing', listing_id=listing_id)
            else:
                message = "Your bidding must be at least equal to the current price."
            context = {"listing": listing,
                        "message": message,
                        "bidding_form": BidForm()
                        }

            return render(request, "auctions/listing.html", context)

        else:
            message = "invalid submission"
            messages.error(request, 'There was an error with your submission.')
    return redirect('listing', listing_id=listing_id)
@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    if request.user != listing.user:
        return HttpResponseForbidden("You are not authorized to close this listing.")
    
    listing.assign_winner()
    listing.status = Listing.CLOSED
    listing.save()
    return redirect('listing', listing_id)
    

@login_required
def modify_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.user != listing.user:
        return HttpResponseForbidden("You are not authorized to modify this listing.")
    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing modified successfully.')
            return redirect('listing', listing_id=listing_id)
        else:
            messages.error(request, 'There was an error with your submission.')
    else:
        form = ListingForm(instance=listing)
    return render(request, "auctions/modify_listing.html", {'form': form, 'listing':listing})

def categories(request):
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request,"auctions/categories.html", context)

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    clistings = category.get_listings()    
    return render(request, "auctions/category.html", {"clistings":clistings,
                                                      "category": category})