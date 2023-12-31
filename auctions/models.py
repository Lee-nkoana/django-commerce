from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class bid(models.Model):
    bid_price = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

    def __str__(self):
        return self.bid_price

class Catagory(models.Model):
    catagoryName = models.CharField(max_length=64)

    def __str__(self):
        return self.catagoryName

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, blank=True, null=True, related_name="catagory")
    price = models.IntegerField(default=0)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    BidActive = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"


