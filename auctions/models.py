
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, URLValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=300) # Increased length

    def __str__(self):
        return self.name
    def get_listings(self):
        return Listing.objects.filter(category=self)

class Listing(models.Model):
    OPEN = 'Open'
    CLOSED = 'CLOSED'
    PENDING = 'PENDING'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
        (PENDING, 'Pending'),
    ]

    user = models.ForeignKey('User', related_name="owned_listings", on_delete=models.CASCADE)
    title = models.CharField(max_length=200) # Increased length
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    image_url = models.URLField(validators=[URLValidator()], blank=True, max_length=500)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    winner = models.ForeignKey('User', related_name="won_listings", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, related_name="listings", on_delete=models.SET_NULL, null=True, blank=True)
    # category = models.CharField(blank=True, default='')  # Optional TextField for category
    cp = None
    def current_price(self):
        bids = self.bids.all()
        if bids:
            self.cp = max(bid.price for bid in bids)
            
        else:
            self.cp = self.starting_bid
        return self.cp
    
    def total_bids(self):
        return self.bids.count()

    def highest_bidder(self):
        bids = self.bids.all()
        if bids:
            highest_bid = max(bids, key=lambda bid: bid.price)
            return highest_bid.user
        else:
            return None
        
    def assign_winner(self):
        self.winner = self.highest_bidder()

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, related_name="watched_by")

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids', default = None)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
    time = models.DateTimeField(default=timezone.now) # Added time field for bid

    def __str__(self):
        return f"Bid on {self.listing.title} by {self.user.username}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments', default = None)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)

    def __str__(self):
        return f"Comment on {self.listing.title} by {self.user.username}"

 


