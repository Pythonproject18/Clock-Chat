from ..models import User
import random
from django.core.mail import send_mail
from django.core.cache import cache  # ✅ Using Django cache instead of memory storage
from django.core.mail import send_mail
from django.conf import settings


def create_user(first_name,middle_name,last_name,email):
    User.objects.create(
        first_name=first_name,
        middle_name= middle_name,
        last_name= last_name,
        email=email
    )
    return

def generate_otp(email):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    cache.set(f"otp_{email}", otp, timeout=300)  # Store OTP in cache for 5 minutes

    # Send OTP via email
    send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,  
            recipient_list=[email],
            fail_silently=False,
        )
    return otp

def user_exists(email):
    return User.objects.filter(email=email).exists()

def get_user(email):
    return User.objects.get(email=email)