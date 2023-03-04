from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse 

# Create your views here.
@csrf_exempt
def data(request):
    return JsonResponse({"hello":"hiii"},safe=False)
