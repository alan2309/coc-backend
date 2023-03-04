from django.urls import path
from . import views

urlpatterns = [
    path('post-review/',views.postReview),
    path('get-reviews/',views.getReviews),
    path('get-companions/',views.getCompanions),
    path('save-trip/',views.saveTrip),
    path('accept-request/',views.acceptReq),
    path('reject-request/',views.rejectReq),
    path('send-request/',views.sendReq),
    path('notifications/',views.notifications),
    path('get-trips/',views.getTrips),
]