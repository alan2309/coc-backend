from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MyUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    profile_img = models.CharField(max_length=255,null=True,blank=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    friends = models.JSONField(default=list,null=True,blank=True)
    home = models.CharField(max_length=100)
    phone = models.IntegerField(null=True,blank=True)
    interests = models.JSONField(null=True,blank=True)
    pending_req = models.JSONField(default=list,null=True,blank=True)
    blocked = models.JSONField(default=list,null=True,blank=True)
    req_sent = models.JSONField(default=list,null=True,blank=True)

    def __str__(self):
        return self.user.first_name

class Trip(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=20)
    location = models.JSONField()
    loc_name = models.CharField(max_length=100,null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)     
    companion = models.JSONField(null=True,blank=True)
    itinerary = models.JSONField(null=True,blank=True)
    feedback = models.IntegerField(default=0)
    pending_req = models.JSONField(null=True,blank=True)
    status = models.IntegerField(default=0) #0-complete 1-ongoing 2-future

    def __str__(self):
        return self.name

class Reviews(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True,blank=True)
    trip = models.ForeignKey(Trip,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=30)
    itinerary = models.JSONField()
    location = models.JSONField()
    loc_name = models.CharField(max_length=20,null=True,blank=True)
    time = models.TimeField(auto_now=True)
    review = models.CharField(max_length=200)
    images = models.JSONField()
    def __str__(self):
        return self.name