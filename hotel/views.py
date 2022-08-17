from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Hotel, Room, Booking, Rating, Like, Comment
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer, CommentSerializer
from permissions import IsAdminOrReadOnly, IsAuthor

class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('name', openapi.IN_QUERY, 'search hotels by name', type=openapi.TYPE_STRING)])

    @action(methods=['GET'], detail=False)
    def search(self, request):
        name = request.query_params.get('name')
        queryset = self.get_queryset()
        if name:
            queryset = queryset.filter(title__icontains=name)
        
        serializer = HotelSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, 200)

    @action(methods=["GET"], detail=False)
    def order_by_rating(self, request):
        queryset = self.get_queryset()

        queryset = sorted(queryset, key=lambda hotel: hotel.average_rating, reverse=True)
        serializer = HotelSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data, 200)

    @action(methods=["GET"], detail=False)
    def order_by_price(self, request):
        queryset = self.get_queryset()

        queryset = sorted(queryset, key=lambda hotel: hotel.price, reverse=True)
        serializer = HotelSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data, 200)

class RoomViewSet(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class CommentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor, IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def toggle_like(request, h_code):
    user = request.user
    hotel = get_object_or_404(Hotel, hotel_code=h_code)

    if Like.objects.filter(user=user, hotel=hotel).exists():
        Like.objects.filter(user=user, hotel=hotel).delete()
    else:
        Like.objects.create(user=user, hotel=hotel)
    return Response("Like toggled", 200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_rating(request, h_code):
    user = request.user
    hotel = get_object_or_404(Hotel, hotel_code=h_code)
    value = request.POST.get("value")

    if not value:
        raise ValueError("Value is required")

    if Rating.objects.filter(user=user, hotel=hotel, value=value).exists():
        rating = Rating.objects.get(user=user, hotel=hotel)
        rating.value = value
        rating.save()
    else:
        Rating.objects.create(user=user, hotel=hotel, value=value)

    return Response("Rating created", 201)

