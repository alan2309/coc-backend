from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse 
import geopy.distance
from rest_framework.parsers import JSONParser
from api.models import Reviews,MyUser,Trip
from .serializers import ReviewSerializer,MyUserSerializer
import datetime

# Create your views here.
@csrf_exempt
def getReviews(request):
    if request.method =="POST":
        data=JSONParser().parse(request)['data']
        lat = data['latitude']
        long = data['longitude']
        reviews = Reviews.objects.all()
        rev_data = []
        for rev in reviews:
            dist = geopy.distance.geodesic((lat,long), (rev.location['latitude'],rev.location['longitude'])).km
            if  dist< 50:
                rev_data.append(rev)
            else:
                print(dist)    

        mydata = ReviewSerializer(rev_data,many=True).data       
        return JsonResponse(mydata,safe=False)

@csrf_exempt    
def postReview(request):
    if request.method == "POST":
        data=JSONParser().parse(request)['data']
        rev = Reviews(user=MyUser.objects.get(id=data['uid'])
                    #   ,trip =Trip.objects.get(id=data['tid']) 
                      ,name="hello",location=data['location'],itinerary = data['location'])
        rev.save()
        return JsonResponse("done",safe=False)
    
@csrf_exempt      
def getCompanions(request):
    if request.method == "POST":
        data=JSONParser().parse(request)['data']
        lat = data['latitude']
        long = data['longitude']
        interests = data['interests']
        d = datetime.datetime.utcnow()
        trips = Trip.objects.filter(end_date__gt=d)
        sort_trip = []
        for trip in trips:
            dist = geopy.distance.geodesic((lat,long), (trip.location['latitude'],trip.location['longitude'])).km
            if  dist< 50:
                sort_trip.append(trip.user)
            else:
                print(dist)
        print(sort_trip)
        sort_users = []
        for u in sort_trip:
            count = 0
            for i in interests:
                if u.interests.count(i)>0:
                    count+=1
            sort_users.append({"user":MyUserSerializer(u).data,"count":count})

        for i in range(0,len(sort_users)-1):  
            for j in range(len(sort_users)-1): 
                if(sort_users[j]['count']<sort_users[j+1]['count']):
                    temp = sort_users[j]  
                    sort_users[j] = sort_users[j+1]  
                    sort_users[j+1] = temp
        return JsonResponse(sort_users,safe=False)    
