from rest_framework import serializers
from api.models import Reviews,MyUser,Trip


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields='__all__'

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields='__all__'    

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields='__all__'             