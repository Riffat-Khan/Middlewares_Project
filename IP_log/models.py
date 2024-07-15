from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
class UserRole(models.Model):
    ROLE = [
        ("Gold" , "gold"),
        ("Silver" , "silver"),
        ("Bronze" , "bronze"),
        ("Unauthenticated", "unauthenticated")
    ]
    
    name = models.CharField(max_length=50, default='')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE)
    

    