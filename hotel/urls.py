from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HotelViewSet, RoomViewSet, CommentViewSet, BookingViewSet, toggle_like, add_rating

router = DefaultRouter()
router.register("hotel", HotelViewSet)
router.register("rooms", RoomViewSet)
router.register("comments", CommentViewSet)
router.register("booking", BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('toggle_like/<int:h_code>/', toggle_like),
    path('add_rating/<int:h_code>/', add_rating),
]
