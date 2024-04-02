from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember, Booking
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render
from .models import Booking
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login


# assuming this is unchanged
def home(request):
    return render(request, 'base/home.html')

@login_required
def who_am_i(request):
    # print the username of the logged-in user to the console
    print(f"Logged in as: {request.user.username}")
    
    # return a simple HttpResponse
    return HttpResponse(f"You are logged in as {request.user.username}")


def student_login(request):
    if request.user.is_authenticated:
        # If already logged in, redirect to bookings
        return redirect('bookings')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # print the received username and password for debugging
        print(f"Attempting to log in with username: {username}, password: {password}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Print debug information about user's existence and group membership
            print(f"User {username} exists. Checking if user is in 'Students' group...")
            if user.groups.filter(name='Students').exists():
                print(f"User {username} is in 'Students' group. Proceeding to log in.")
                login(request, user)
                return redirect('bookings')
            else:
                print(f"User {username} is not in 'Students' group.")
        else:
            print(f"User {username} does not exist or password is incorrect.")
        
        # if authentication fails, return to the same login page with an error message
        return render(request, 'base/student_login.html', {'error': 'Invalid credentials or not a student'})
    else:
        # for a GET request, just display the login form
        return render(request, 'base/student_login.html')




def teacher_login(request):
    if request.user.is_authenticated:
        # if already logged in, redirect to teacher dashboard
        return redirect('teacher_dashboard')  
    if request.method == 'POST':
        username = request.POST.get('username')  # match the form field name
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='Teachers').exists():
            login(request, user)
            return redirect('teacher_dashboard')  # redirect to teacher dashboard
        else:
            return render(request, 'base/teacher_login.html', {'error': 'Invalid credentials or not a teacher'})
    else:
        return render(request, 'base/teacher_login.html')
    
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        # create the user
        user = User.objects.create_user(username=username, password=password)
        
        # assign the user to the correct group and define redirect URL based on role
        redirect_url = 'student_dashboard'  # default to student dashboard
        if role == 'student':
            group = Group.objects.get(name='Students')
        elif role == 'teacher':
            group = Group.objects.get(name='Teachers')
            redirect_url = 'teacher_dashboard'  # change redirect URL for teachers
        user.groups.add(group)
        user.save()

        # authenticate and login the user
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(redirect_url)  # redirect based on the role
    
    return render(request, 'signup')  # render a signup form template



@login_required
def teacher_dashboard(request):
    
    bookings = Booking.objects.all().order_by('-booking_date') 
    
   
    
    context = {
        'message': "Welcome to your Dashboard",
        'bookings': bookings,
        
    }
    return render(request, 'base/teacher_dashboard.html', context)


# User logout view
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def view_bookings(request):
    # Retrieve bookings for the current user
    user_bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'base/bookings.html', {'bookings': user_bookings})




@login_required
def create_booking(request):
    # Ensure only authenticated users can create bookings
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to create a booking.")
    
    if request.method == "POST":
        booking_date_str = request.POST.get('booking_date')
        teacher_id = request.POST.get('teacher')
        
        try:
            # Attempt to convert the booking date to a datetime object
            booking_date = datetime.strptime(booking_date_str, "%Y-%m-%dT%H:%M")
            # Ensure the selected teacher exists
            teacher = User.objects.get(id=teacher_id)
            
            # Create the Booking
            booking = Booking.objects.create(
                user=request.user,
                teacher=teacher,
                booking_date=booking_date,
                confirmed=False
            )
            booking.save()
            return redirect('bookings')
        except ValueError:
            # handle incorrect date format
            return render(request, 'base/create_booking.html', {
                'error': 'Invalid date format. Please use YYYY-MM-DDTHH:MM format.',
                'teachers': User.objects.filter(groups__name='Teachers')
            })
        except User.DoesNotExist:
            #handle case where the selected teacher does not exist
            return render(request, 'base/create_booking.html', {
                'error': 'Selected teacher does not exist.',
                'teachers': User.objects.filter(groups__name='Teachers')
            })
    else:
        # for GET requests, display the booking form with the list of teachers
        return render(request, 'base/create_booking.html', {
            'teachers': User.objects.filter(groups__name='Teachers')
        })
    
def change_booking_status(request, booking_id):
    
    return redirect('bookings')  # redirect to bookings page after

@login_required
def toggle_booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check: ensure the current user is the teacher for the booking
    if booking.teacher != request.user:
        return HttpResponseForbidden("You do not have permission to change this booking's status.")

    # Toggle confirmation status
    booking.confirmed = not booking.confirmed
    booking.save()
    
    return redirect('teacher_dashboard')  # Redirect back to the teacher dashboard

def getToken(request):
    appId = 'cb3fa3b62ac94450847c7b1c7d2e35b1'
    appCertificate = '58686b768c6c44ce802ea61da921b6b4'
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse ({'token': token, 'uid': uid}, safe=False)

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)