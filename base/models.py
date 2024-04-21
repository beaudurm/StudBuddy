from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random
import string



# Create your models here.

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_bookings',
        verbose_name='Student'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_bookings',
        verbose_name='Teacher',
        null=True,  # allowing null values for development/testing purposes
    )
    booking_date = models.DateTimeField()
    confirmed = models.BooleanField(default=False)
    passphrase = models.CharField(max_length=4, blank=True)  # passphrase

    def save(self, *args, **kwargs):
        if not self.passphrase:  
            letters = random.choices(string.ascii_letters, k=2)
            digits = random.choices(string.digits, k=2)
            self.passphrase = ''.join(random.sample(letters + digits, 4))  # booking key randomiser
        super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        teacher_name = self.teacher.username if self.teacher else "Unassigned"
        return f"Booking for {self.user.username} with {teacher_name} on {self.booking_date}"
