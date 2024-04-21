from django.contrib import admin

# Register your models here.
from .models import RoomMember, Booking


admin.site.register(RoomMember)

# Optional: Create a custom admin interface for Booking
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher', 'booking_date', 'confirmed')  # Customize list display
    list_filter = ('confirmed', 'booking_date')  # enable filtering by these fields
    search_fields = ('user__username', 'teacher__username')  # enable search  usernames

admin.site.register(Booking, BookingAdmin)  # Register Booking with admin interface