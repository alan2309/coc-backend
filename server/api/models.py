from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MyUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Trip(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=20)
    location = models.JSONField()
    start_date = models.DateField()
    end_date = models.DateField()    
    companion = models.JSONField()
    itineary = models.JSONField()
    feedback = models.JSONField()
    status = models.IntegerField() #0-complete 1-ongoing 2-future