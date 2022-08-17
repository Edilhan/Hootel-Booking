from rest_framework import serializers
from .models import Hotel,Room,Booking,Comment, Like, Rating
from datetime import datetime

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["rooms"] = RoomSerializer(instance.rooms.all(), many=True).data
        rep["rating"] = instance.average_rating
        rep["user_rating"] = 0

        request = self.context.get("request")

        if request.user.is_authenticated:
            if Rating.objects.filter(user=request.user, hotel=instance).exists():
                rating = Rating.objects.get(user=request.user, hotel=instance)
                rep["user_rating"] = rating.value

        return rep

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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["comments"] = CommentSerializer(instance.comments.all(), many=True).data
        rep["likes"] = instance.likes.all().count()
        rep["liked_by_user"] = False

        request = self.context.get("request")

        if request.user.is_authenticated:
            rep["liked_by_user"] = Like.objects.filter(user=request.user, room=instance).exists()

        bookings = Booking.objects.filter(room=instance.room_id)
        for b in bookings:
            if b.arrival_time <= datetime.now().time() < b.departure_time:
                rep["availability"] = False

        return rep


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude =['user']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        rep["user"] = instance.user.email
        return rep
        
