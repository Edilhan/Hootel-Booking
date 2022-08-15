from rest_framework import serializers
from .models import Hotel,Room,Booking

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

    def to_representation(self, instance:Hotel):
        rep = super().to_representation(instance)
        rep['rating'] = instance.average_rating

        request = self.context.get('request')
        return rep
        