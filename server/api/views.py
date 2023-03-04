from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse 
import geopy.distance
from rest_framework.parsers import JSONParser
from api.models import Reviews,MyUser,Trip
from .serializers import ReviewSerializer

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
            if geopy.distance.geodesic((lat,long), (rev.location['latitude'],rev.location['longitude'])).km < 20:
                rev_data.append(rev)

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
