from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, bid, Catagory
from django import forms

#default landing, all active listings are visible
def index(request):
        activelisting = Listing.objects.filter(BidActive=True)
        allCatagories = Catagory.objects.all()
        return render(request, "auctions/index.html", {
            "catagories" : allCatagories,
            "listings" : activelisting
    })


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

    #creating a new listing

@login_required
def new_listing(request):
    if request.method == "GET":
        allCatagories = Catagory.objects.all()
        return render(request, "auctions/new_listing.html", {
            "catagories" : allCatagories
        })
    else:
        if request.method == "POST":
            #getting the information from the form
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            catagory = request.POST.get('catagory')
            image_url = request.POST.get('image_url')
            #get current user and the catagory data
            catagoryData = Catagory.objects.get(catagoryName=catagory)
            currentuser = request.user         
           
            #create a bid object
            bidObj = bid(bid_price=int(price), user=currentuser)
            bidObj.save()

           #create a new listing object
            newListing = Listing(
                title=title,
                description=description,
                price=bidObj.bid_price,
                catagory=catagoryData,
                image_url=image_url,
                owner=currentuser
                )
            
            newListing.save()

            return HttpResponseRedirect(reverse("index"))

#password for superuser and name:
#NAME: main password: M_123456

#Creating the watchlist for the user
def watchlist(request):
    currentUser = request.user
    listing = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings" : listing
    })

 #adding a listing to user watchlist   
def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

#function to remove listing from user watchlist    
def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

#function to filter through the different catagories
def filtercatagories(request):
    if request.method == "POST":
        categoryFromForm = request.POST.get('catagory')
        catagory = Catagory.objects.get(catagoryName=categoryFromForm)
        activelisting = Listing.objects.filter(BidActive=True, catagory=catagory)
        allCatagories = Catagory.objects.all()
        return render(request, "auctions/filtercatagories.html", {
            "catagories" : allCatagories,
            "listings" : activelisting
    })

#Creating the listing object
def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, ("auctions/listing.html"), {
        "listing" : listingData,
        "allComments" : allComments,
        "isListingWatchlist" : isListingWatchlist,
        "isOwner" : isOwner
    })

#Adding a new bid to the listing
def addBid(request, id):
    newBid = request.POST.get('newBid')
    listingData = Listing.objects.get(pk=id)
    isListingWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    if int(newBid) > listingData.price:
        updateBid =  bid(user=request.user, bid_price=int(newBid))
        updateBid.save()
        listingData.price = updateBid.bid_price
        listingData.save()
        return render(request, ("auctions/listing.html"), {
        "listing" : listingData,
        "message" : "Bid Success",
        "update" : True,
        "allComments" : allComments,
        "isListingWatchlist" : isListingWatchlist,
        "isOwner" : isOwner
        })
    else:
         return render(request, ("auctions/listing.html"), {
        "listing" : listingData,
        "message" : "Bid Failed",
        "update" : False,
        "allComments" : allComments,
        "isListingWatchlist" : isListingWatchlist,
        "isOwner" : isOwner
        })

#adding coments on specific listing
def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST.get('comment')

    comment = Comment(
        author = currentUser,
        listing = listingData,
        message = message
    )

    comment.save()

    return HttpResponseRedirect(reverse("listing", args=(id,)))

#close listing if user is owner of listing
def closeListing(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.BidActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    isListingWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    return render(request, ("auctions/listing.html"), {
        "listing" : listingData,
        "allComments" : allComments,
        "isListingWatchlist" : isListingWatchlist,
        "isOwner" : isOwner,
        "update" : True,
        "message" : "Auction has been closed."
    })