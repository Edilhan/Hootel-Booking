from rest_framework import serializers
from .models import Hotel,Room,Booking,Comment

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["comments"] = CommentSerializer(instance.comments.all(), many=True).data
        rep["likes"] = instance.likes.all().count()
        rep["rating"] = instance.average_rating
        rep["liked_by_user"] = False
        rep["user_rating"] = 0

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude =['user']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        rep["user"] = instance.user.email
        return rep


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
    