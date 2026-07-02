from django.contrib import admin
from .models import Room, Booking
# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name','capacity', 'location')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'title', 'user', 'start_time', 'end_time')
