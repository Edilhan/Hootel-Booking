from rest_framework.viewsets import ModelViewSet

from .models import Hotel, Room, Booking, Rating, Like, Comment
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer, CommentSerializer
