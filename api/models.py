from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MyUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    userRole = models.IntegerField()
    phoneNumber = models.IntegerField()
    userImage = models.CharField()
    verified = models.CharField()
    secretKey = models.CharField()
    history = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    cName = models.CharField()
    cDescription = models.CharField()
    cImage = models.CharField(blank=True,null=True)
    cStatus = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.cName

class Customize(models.Model):
    slideImage = models.CharField(blank=True,null=True)
    firstShow = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.firstShow
    
class Order(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    allProduct = models.JSONField()
    amount = models.IntegerField()
    transactionId = models.CharField()
    address = models.CharField()
    phone = models.IntegerField()
    status = models.CharField(default='Not processed', choices=(
        ('Not processed','Not processed'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.firstShow
    
class Product(models.Model):
    pName = models.CharField()
    pDescription = models.CharField()
    pPrice = models.DecimalField(max_digits=8,decimal_places=2)
    pSold = models.IntegerField(default=0)
    pQuantity = models.IntegerField(default=0)
    pCategory = models.ForeignKey(Category,on_delete=models.SET_NULL)
    pImages = models.JSONField()
    pOffer = models.CharField()
    pRatingsReviews = models.JSONField()
    pStatus = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.transactionId