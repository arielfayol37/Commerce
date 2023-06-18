
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, URLValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200) # Increased length

    def __str__(self):
        return self.name

class Listing(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Pending', 'Pending'),
    ]

    user = models.ForeignKey('User', related_name="owned_listings", on_delete=models.CASCADE)
    title = models.CharField(max_length=200) # Increased length
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    image_url = models.URLField(validators=[URLValidator()], blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    winner = models.ForeignKey('User', related_name="won_listings", on_delete=models.SET_NULL, null=True, blank=True)

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

 


"""
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Listing(models.Model):
    user = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def html(self):
        formatted_description = format_html("<p>{}</p>", self.description)
        formatted_title = format_html("<h2>{}</h2>", self.title)
        formatted_starting_bid = format_html("<p>Starting Bid: ${}</p>", self.starting_bid)
        formatted_category = format_html("<p>Category: {}</p>", self.category)
        formatted_image = format_html("<img class= 'img-listing' src='{}' alt= '{} Image'\
                                      >",\
                                       self.image_url, self.title)

        return format_html(
            "{}\n{}\n{}\n{}\n{}",
            formatted_title,
            formatted_image,
            formatted_description,
            formatted_starting_bid,
            formatted_category
            
        )

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, related_name="watched_by")
   
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids', default = None)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)

    def __str__(self):
        return f"Bid on {self.listing.title} by {self.user.username}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments', default = None)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)

    def __str__(self):
        return f"Comment on {self.listing.title} by {self.user.username}"

class Listing(models.Model):
    user= models.ForeignKey(User, related_name = "listings", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.TextField()
    category = models.TextField()
    current_price = models.ForeignKey(Bid)
    
    def __str__(self):
        return f"title: {self.title} <hr/> description: {self.description}"

class Bid(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
"""

