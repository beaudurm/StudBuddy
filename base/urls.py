from django.urls import path
from . import views
from .views import who_am_i 
from .views import user_logout 
from .views import signup

urlpatterns = [
    # home page
    path('', views.home, name='home'),
    
    # authentication URLs
    path('student_login/', views.student_login, name='student_login'),  # Student login
    path('teacher_login/', views.teacher_login, name='teacher_login'),  # Teacher login
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('whoami/', who_am_i, name='who_am_i'),


     # teacher dashboard
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    
    
    # booking 
    path('create_booking/', views.create_booking, name='create_booking'),
    path('bookings/', views.view_bookings, name='bookings'),
    path('change_booking_status/<int:booking_id>/', views.change_booking_status, name='change_booking_status'),
    path('booking/confirm/<int:booking_id>/', views.toggle_booking_confirmation, name='toggle_booking_confirmation'),
    
    # lobby and room URLs for video streamer
    path('lobby/', views.lobby, name='lobby'),
    path('room/', views.room, name='room'),
    
    # token generation for Agora
    path('get_token/', views.getToken, name='get_token'),
    
    #room member actions
    path('create_member/', views.createMember, name='create_member'),
    path('get_member/', views.getMember, name='get_member'),
    path('delete_member/', views.deleteMember, name='delete_member'),
]
