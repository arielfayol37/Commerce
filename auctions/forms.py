from django import forms
from .models import Listing, Comment, Bid

class ListingForm(forms.ModelForm):
    category = forms.CharField(required=False)
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']