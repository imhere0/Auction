from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment, Watchlist, Winner
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def index(request):
    winner_list = []
    posts = []

    try:
        winnerobject0 = Winner.objects.all()
    except:
        winnerobject0 = None

    if winnerobject0:
        
        for element in winnerobject0:
            winner_list.append(element.id)

        listingobj0 = Listing.objects.all()
        
        for item in listingobj0:
            if item.id not in winner_list:
                posts.append(item)

        return render(request, "auctions/index.html", {
            "posts": posts
        })


    listingobj1 = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "posts": listingobj1
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

@login_required
def createListing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["initialbid"]

        if not title or not description or not price :
            return render(request, "auctions/create_listing.html", {
                "message" : " Must provide the Mandotary Form Field."
            })

        category = request.POST["category"]
        image = request.POST["iurl"]
        current_user = request.user

    
        listingobj = Listing.objects.create(title = title, description = description, price = price, category = category, link = image, seller = current_user.username)
        listingobj.save()

        all_objects = Listing.objects.all()

        return render(request, "auctions/index.html",  {
            "posts": all_objects
        })
    else:
        return render(request, "auctions/create_listing.html")



def activeListing(request):

    winner_list = []
    posts = []

    try:
        winnerobject0 = Winner.objects.all()
    except:
        winnerobject0 = None

    if winnerobject0:
        
        for element in winnerobject0:
            winner_list.append(element.id)

        listingobj0 = Listing.objects.all()

        for item in listingobj0:
            if item.id not in winner_list:
                posts.append(item)

        return render(request, "auctions/index.html", {
            "posts": posts
        })


    listingobj1 = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "posts": listingobj1
    })


def closedListing(request):
    winner_list = []
    posts = []

    try:
        winnerobject0 = Winner.objects.all()
    except:
        winnerobject0 = None

    if winnerobject0:
        
        for element in winnerobject0:
            winner_list.append(element.id)

        listingobj0 = Listing.objects.all()

        for item in listingobj0:
            if item.id in winner_list:
                posts.append(item)

        return render(request, "auctions/closedlisting.html", {
            "posts": posts
        })
    else:
        return render(request, "auctions/closedlisting.html",{
            "message":"No listing has been closed"
        })    


@login_required
def categories(request):
    
        category_list = []
        listobjects1 = Listing.objects.all()

        for element in listobjects1:
            if element.category not in category_list:
                category_list.append(element.category)

        return render(request, "auctions/categories.html",{
            "categories":category_list
        })



@login_required
def title(request, id):
    
    listingobject = Listing.objects.get(id = id)

    # except:
    #     all_objects1 = Listing.objects.all()
    #     return render(request, "auctions/index.html",  {
    #         "posts": all_objects1
    #     })
    current_user = request.user.username        


    if request.method == "POST":

        try:
            bid = request.POST["bid"]
        except:
            bid = None

        if bid:
            if int(bid) <= int(listingobject.price):
                raise PermissionDenied("The Bid must be greater then the current price of the associated object")
            try:    
                biddingobject = Bid.objects.get(listingid = id)
            except:
                biddingobject = None

            if biddingobject:
                biddingobject.delete()

            biddingobject1 = Bid.objects.create(listingid = id, user = current_user, amount = bid)
            biddingobject1.save()
            

            listingobject.price = bid
            listingobject.save()

        try:
            comment = request.POST["comment"]
        except:
            comment = None

        if comment:
            commentobject = Comment.objects.create(user = current_user, listingid = id, comment = comment)
            commentobject.save()

        try:
            add = request.POST["add"]
        except:
            add = None

        try:
            remove = request.POST["remove"]
        except:
            remove = None

        if add:
            seller = listingobject.seller
            created_time = listingobject.time
            image = listingobject.link
            item_price = listingobject.price
            user = current_user
            item_title = listingobject.title

            watchlistobject = Watchlist.objects.create(user = current_user, seller = seller, time = created_time,  title = item_title, price = item_price, listingid = id,image = image)
            watchlistobject.save()

        elif remove:
                watchlistobject2 = Watchlist.objects.get(user = current_user, listingid = id)
                watchlistobject2.delete()

        try:
            close_bid = request.POST["bidclose"]
        except:
            close_bid = None

        if close_bid:

            try:
                biddingobject1 = Bid.objects.get(listingid = id)
            except:
                biddingobject1 = None

            if biddingobject1:
                bid_winner = biddingobject1.user

                winnerobject = Winner.objects.create(price = listingobject.price, listingid = id, winner = bid_winner, owner = listingobject.seller)
                winnerobject.save()                                

        return HttpResponseRedirect(reverse("title", args = (id,)))

    else:
        
        try:
            watchlistobject2 = Watchlist.objects.get(listingid = id, user = current_user)
        except:
            watchlistobject2 = None

        add_message = "This is add message"

        try:
            commentobject1 = Comment.objects.filter(listingid = id)
        except:
            commentobject1 = None

        try:        
            biddingobject2 = Bid.objects.get(listingid = id)
        except:
            biddingobject2 = None
        bid_message = "This is bid message"            

        try:
            winnerobject1 = Winner.objects.get(listingid = id)

        except:
            winnerobject1 = None

        if winnerobject1:
            return render(request, "auctions/title.html",{
                "post":listingobject,"id":id,"winner":winnerobject1
            })

                            

        if watchlistobject2 == None:
            return render(request, "auctions/title.html",{
                "post":listingobject,"id":id,"comments":commentobject1,"bids":biddingobject2,"bid_message":bid_message
            })

        return render(request, "auctions/title.html",{
            "post":listingobject,"id":id,"comments":commentobject1,"bids":biddingobject2,"bid_message":bid_message,"add_message":add_message
        })


@login_required
def watchlist(request, username):
    current_user = request.user.username
    watchlistobj = Watchlist.objects.filter(user = current_user)
    return render(request, "auctions/watchlist.html",{
        "watchlists":watchlistobj
    })


@login_required
def remove(request, id):
            

        listingobject1 = Listing.objects.get(id = id)
        listingobject1.delete()
        return render(request, "auctions/index.html",{
            "posts": Listing.objects.all()
        })

@login_required
def categoricalactivelisting(request, category):
    winner_list0 = []
    posts0 = []
    try:
        lastwinnerobject = Winner.objects.all()
    except:
        lastwinnerobject = None

    if lastwinnerobject:
        for element in lastwinnerobject:
            winner_list0.append(element.id)
        lastlistingobject0 = Listing.objects.filter(category = category)
        for item in lastlistingobject0:
            if item.id not in winner_list0:
                posts0.append(item)

        return render(request, "auctions/categoricalactivelisting.html",{
            "items":posts0
        } )

    lastlistingobject = Listing.objects.filter(category = category)
    return render(request, "auctions/categoricalactivelisting.html",{
        "items":lastlistingobject
    } )


    







            



