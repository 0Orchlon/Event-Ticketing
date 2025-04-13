# tickets/models.py

from django.db import models

# User model
class User(models.Model):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('EventOrganizer', 'EventOrganizer'),
        ('Admin', 'Admin'),
    ]
    
    username = models.CharField(max_length=50, unique=True)
    gmail = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phonenumber = models.CharField(max_length=20, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    profilepictureurl = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')
    is_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# Event model
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Booking model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    
    def __str__(self):
        return f'{self.user.username} booked {self.event.name}'
