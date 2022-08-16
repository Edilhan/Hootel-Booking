from django.db import models

from account.models import User

CITY_CHOICES = [
    ("Бишкек", "Бишкек"), 
    ("Ош", "Ош"), 
    ("Чолпон-Ата", "Чолпон-Ата")]

ROOM_TYPE_CHOICES = []

ROOM_OCCUPANCY_CHOICES = []

ROOM_STATUS = [
    ("1", "available"), 
    ("2", "not available")
]
    
class Hotel(models.Model):
    hotel_code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='hotels', blank=True, null=True)
    address = models.CharField(max_length=200)
    postcode = models.IntegerField()
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    num_of_rooms = models.IntegerField()
    phone_number = models.IntegerField()
    star_rating = models.IntegerField()

class Room(models.Model):
    room_number = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='rooms', blank=True, null=True)
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES)
    status = models.CharField(choices=ROOM_STATUS, max_length=15)
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    max_occupancy = models.IntegerField(choices=ROOM_OCCUPANCY_CHOICES)
    
class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='bookings', on_delete=models.CASCADE)
    guest_id = models.ManyToManyField(User, related_name='bookings')
    room_number = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
    booking_datetime = models.DateTimeField(auto_now_add=True)
    arrival_datetime = models.DateTimeField()
    departure_datetime = models.DateTimeField()

class Comment(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    quest = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    hotel_code = models.ForeignKey(Hotel, related_name='comments', on_delete=models.CASCADE)

class Like(models.Model):
    quest = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='likes', on_delete=models.CASCADE)

class Rating(models.Model):
    quest = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])

