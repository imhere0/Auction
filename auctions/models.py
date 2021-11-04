from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.CharField(max_length = 64)
    title = models.CharField(max_length = 64)
    description = models.TextField()
    price = models.CharField(max_length=64)
    category = models.CharField(max_length = 64, default = None, blank = True, null = True)
    time = models.DateTimeField(auto_now_add= True)
    link = models.CharField(max_length = 200, default = None, blank = True, null = True)

    

class Bid(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    amount = models.CharField(max_length = 64)
    


class Comment(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add= True)

class Watchlist(models.Model):
    user = models.CharField(max_length = 64)
    seller = models.CharField(max_length = 64)
    time = models.DateTimeField()
    image =  models.CharField(max_length = 200, default = None, blank = True, null = True)
    price = models.CharField(max_length = 64)
    listingid = models.IntegerField()
    title = models.CharField(max_length= 64,default = "Not Added")   



class Winner(models.Model):
    winner = models.CharField(max_length = 64)
    owner = models.CharField(max_length = 64)
    price = models.CharField(max_length = 64)
    listingid = models.IntegerField()
    time = models.DateTimeField(auto_now_add = True)  