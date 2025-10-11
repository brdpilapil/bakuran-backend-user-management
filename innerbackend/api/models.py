from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ("owner", "Owner"),
    ("admin", "Admin"),
    ("waiter", "Waiter"),
    ("cashier", "Cashier"),
]

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="waiter")
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


    def __str__(self):
        return self.username
