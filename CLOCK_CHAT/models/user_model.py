from django.db import models
from django.contrib.auth.models import AbstractUser
from ..constants import Gender, Role

class User(AbstractUser):
    first_name = models.CharField(max_length=10)
    middle_name = models.CharField(max_length=10, blank=True, null=True)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=100,blank=True,null = True)
    profile_photo_url = models.URLField(max_length=255, blank=True, null=True)
    
    gender = models.IntegerField(
        choices=[(gen.value, gen.name) for gen in Gender],
        null=True, blank=True
    )
    role = models.IntegerField(
        choices=[(r.value, r.name) for r in Role],
        null=True, blank=True,
        db_default=Role.END_USER.value
    )

    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Remove default Django groups and permissions
    groups = None
    user_permissions = None
    password = None  
    username = models.CharField(max_length=250, blank=True, null=True)
    is_staff = models.BooleanField(default=False, blank=True)
    is_superuser = models.BooleanField(default=False, blank=True)

    # Use Email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  

    def set_password(self, raw_password):
        """Override set_password to prevent password creation."""
        return None

    def check_password(self, raw_password):
        """Override check_password to always fail."""
        return False

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"ID: {self.id}, Email: {self.email}, Active: {self.is_active}"
