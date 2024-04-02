from django.contrib import admin

# Register your models here.
from .models import RoomMember, Booking


admin.site.register(RoomMember)

# Optional: Create a custom admin interface for Booking
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher', 'booking_date', 'confirmed')  # Customize the list display
    list_filter = ('confirmed', 'booking_date')  # Enable filtering by these fields
    search_fields = ('user__username', 'teacher__username')  # Enable search by usernames

admin.site.register(Booking, BookingAdmin)  # Register Booking with the custom admin interface