from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse 
import geopy.distance
from rest_framework.parsers import JSONParser
from api.models import Reviews,MyUser,Trip
from .serializers import ReviewSerializer,MyUserSerializer,TripSerializer
import datetime
from django.contrib.auth.models import User,auth
from django.contrib.auth.hashers import make_password

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
        trip = Trip.objects.get(id = data['tid'])
        rev = Reviews(user=MyUser.objects.get(id=data['uid'])
                      ,trip =Trip.objects.get(id=data['tid']) 
                      ,name=trip.name,location=data['location'],itinerary = trip.itinerary,
                      loc_name = trip.loc_name,review = "good")
        rev.save()
        return JsonResponse("done",safe=False)
    
@csrf_exempt      
def getCompanions(request):
    if request.method == "POST":
        data=JSONParser().parse(request)['data']
        lat = data['latitude']
        long = data['longitude']
        user = MyUser.objects.get(id = data['uid'])
        interests = data['interests']
        d = datetime.datetime.utcnow()
        trips = Trip.objects.filter(end_date__gt=d).exclude(user = user)
        sort_trip = []
        for trip in trips:
            dist = geopy.distance.geodesic((lat,long), (trip.location['latitude'],trip.location['longitude'])).km
            if  dist< 50:
                sort_trip.append(trip.user)
            else:
                print(dist)
        print(sort_trip)
        print(user.pending_req)
        for i in user.friends:
            for user in sort_trip:
                if user.email == i:
                    sort_trip.remove(user)
        for i in user.pending_req:
            for user in sort_trip:
                if user.email == i:
                    sort_trip.remove(user)
        for i in user.req_sent:
            for user in sort_trip:
                if user.email == i:
                    sort_trip.remove(user)
        for i in user.blocked:
            for user in sort_trip:
                if user.email == i:
                    sort_trip.remove(user)                        
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

@csrf_exempt 
def saveTrip(request):
    if request.method == "POST":
        data=JSONParser().parse(request)['data']
        trip = Trip(user = MyUser.objects.get(id = data['uid']),
                    name = data['name'],
                    location = data['location'],
                    loc_name = data['loc_name'],
                    start_date = data['start_date'],
                    end_date = data['end_date'],
                    itinerary = data['itinerary'],
                    )
        trip.save()
        return JsonResponse(TripSerializer(trip).data,safe=False)     

@csrf_exempt  
def sendReq(request):
    if request.method == "POST":
        data=JSONParser().parse(request)['data']
        user = MyUser.objects.get(id = data['uid'])
        user.req_sent.append(data['email'])
        user.save()
        print(user)
        fr = MyUser.objects.get(email = data['email'])
        fr.pending_req.append(user.email)
        fr.save()
        print(fr)
        return JsonResponse("done",safe=False)

@csrf_exempt  
def notifications(request):
    data=JSONParser().parse(request)['data']
    user = MyUser.objects.get(id= data['uid'])
    reqs_data=[]
    for i in user.pending_req:
        reqs = {} 
        reqs['name'] = MyUser.objects.get(email = i).name
        reqs["email"]=i
        reqs_data.append(reqs)
    user_data = MyUserSerializer(user).data
    return JsonResponse({"data":user_data,"reqs":reqs_data},safe=False)

@csrf_exempt  
def acceptReq(request):
    if request.method == "POST":
        data=JSONParser().parse(request)['data']
        user = MyUser.objects.get(id=data['uid'])
        user.pending_req.remove(data['email'])
        user.friends.append(data['email'])
        user.save()
        user2 = MyUser.objects.get(email = data['email'])
        user2.req_sent.remove(user.email)
        user2.friends.append(user.email)
        user2.save()
        return JsonResponse({"data":"Success"},safe=False)

@csrf_exempt  
def rejectReq(request):
    if request.method == "POST":
        data=JSONParser().parse(request)['data']
        user = MyUser.objects.get(data['uid'])
        user.pending_req.remove(data['email'])
        user.blocked.append(data['email'])
        user.save()
        user2 = MyUser.objects.get(email = data['email'])
        user2.req_sent.remove(user.email)
        user2.save()
        return JsonResponse({"data":"Success"},safe=False)

@csrf_exempt
def getTrips(request):
    if request.method == "POST":
        data=JSONParser().parse(request)['data']
        trips = Trip.objects.filter(user = MyUser.objects.get(id = data['uid']))
        d = datetime.datetime.utcnow()
        trips_on = trips.filter(start_date__lte = d,end_date__gt=d)
        trips_done = trips.filter(end_date__lte=d)
        trips_planned = trips.filter(start_date__gt = d)
        return JsonResponse({
            "ongoing": TripSerializer(trips_on,many=True).data,
            "planned":TripSerializer(trips_planned,many=True).data,
            "completed":TripSerializer(trips_done,many=True).data
            },safe=False)
    
@csrf_exempt    
def login(request):
     if request.method == 'POST' :
        data=JSONParser().parse(request)['data']
        username = data['username']
        password = data['password']
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(request,user)
            #return JsonResponse({"status":'done',"user":user},safe=False)
            myuser = MyUser.objects.get(user=user)
            user_data = MyUserSerializer(myuser).data
            return JsonResponse(user_data,safe=False)
        else:
            return JsonResponse({"status":'error'},safe=False)

@csrf_exempt
def regsiter(request):
    if request.method=="POST":
        data=JSONParser().parse(request)['data']
        print(data)
        
        user=User.objects.filter(email=data["email"])
        if not user.exists():
            user=User(email=data["email"],first_name=data["name"],password=make_password(data["password"]),username=data["username"])
            myuser=MyUser(user=user,email=data["email"],age=data["age"],gender=data["gender"],home=data["home"],interests=data["interests"],phone=data["phone"],profile_img=data["profile_img"])
            user.save()
            myuser.save()
        
            

        return JsonResponse({"data":"Success"},safe=False)
                    