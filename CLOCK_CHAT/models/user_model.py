from django.db import models
from django.contrib.auth.models import AbstractUser
from ..constants import Gender, Role

class User(AbstractUser):
    first_name = models.CharField(max_length=10)
    middle_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    profile_photho_url = models.URLField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(
        choices=[(gen.value, gen.name) for gen in Gender],
        null=True,blank=True
    )
    role = models.IntegerField(
        choices=[(r.value, r.name) for r in Role],
        null=True,blank=True,
        db_default=Role.END_USER.value
    )

    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Fields required for Abstract User
    groups = None
    user_permissions = None
    username = models.CharField(max_length=250, blank=True, null=True)
    is_staff = models.BooleanField(db_default=False, blank=True)
    is_superuser = models.BooleanField(db_default=False, blank=True)

    # Use Email as the username field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"