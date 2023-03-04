from django.urls import path
from . import views

urlpatterns = [
    path('post-review/',views.postReview),
    path('get-reviews/',views.getReviews),
    path('get-companions/',views.getCompanions),
]