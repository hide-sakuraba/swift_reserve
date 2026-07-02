from django.urls import path
from .views import HomeView, RoomDetailView, get_bookings

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('room/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('api/bookings/<int:pk>/', get_bookings, name='get_bookings'), # JSON用
]