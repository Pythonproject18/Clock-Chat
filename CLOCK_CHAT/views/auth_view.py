from django.views import View
import random
import time
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.core.cache import cache  # ✅ Using Django cache instead of memory storage
from ..models import User
from ..services import auth_service
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
from django.contrib.auth import logout



@method_decorator(csrf_exempt, name='dispatch')
class OtpSendView(View):
    def post(self, request):
        """Sends OTP to user's email."""
        email = request.POST.get("email")
        if not email:
            return JsonResponse({"status": "error", "message": "Email is required"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already exists"}, status=400)

        otp = random.randint(100000, 999999)
        cache.set(email, {"otp": otp, "verified": False, "timestamp": time.time()}, timeout=300)  # ✅ Store OTP in cache

        print(f"Your OTP for {email} is: {otp}")

        auth_service.generate_otp(email)

        return JsonResponse({"status": "success", "message": f"OTP sent to {email}"}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class OtpVerifyView(View):
    def post(self, request):
        """Verifies OTP entered by the user."""
        email = request.POST.get("email")
        otp = request.POST.get("otp")

        if not email or not otp:
            return JsonResponse({"status": "error", "message": "Email and OTP are required"}, status=400)

        otp_data = cache.get(email)
        if not otp_data:
            return JsonResponse({"status": "error", "message": "OTP expired or not found"}, status=400)

        stored_otp = otp_data["otp"]

        if str(stored_otp) == str(otp):
            cache.set(email, {"otp": stored_otp, "verified": True}, timeout=300)  # ✅ Mark OTP as verified
            return JsonResponse({"status": "success", "message": "OTP verified"}, status=200)

        return JsonResponse({"status": "error", "message": "Invalid OTP"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    def get(self, request):
        return render(request, 'auth/signup.html')

    def post(self, request):
        """Registers user after OTP verification."""
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name", "")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if not first_name or not last_name or not email:
            return JsonResponse({"status": "error", "message": "All required fields must be filled"}, status=400)

        otp_data = cache.get(email)
        if not otp_data or not otp_data["verified"]:
            return JsonResponse({"status": "error", "message": "OTP verification required"}, status=400)

        # Create user
        otp=auth_service.create_user(first_name, middle_name, last_name, email)
        print(otp)
        # Clean up OTP from cache
        cache.delete(email)

        return JsonResponse({"status": "success", "message": "User registered successfully", "redirect": "/sign-in/"})



logger = logging.getLogger(__name__)
class SendOTPView(View):
    def post(self, request):
        email = request.POST.get("email")
        purpose = request.POST.get("purpose")
        
        logger.debug(f"OTP Request Received - Email: {email}, Purpose: {purpose}")

        user_exists = User.objects.filter(email=email).exists()

        if purpose == "signup" and user_exists:
            logger.warning(f"Signup attempt with existing email: {email}")
            return JsonResponse({"status": "error", "message": "Email already registered."})
        
        if purpose == "login" and not user_exists:
            logger.warning(f"Login attempt with non-existent email: {email}")
            return JsonResponse({"status": "error", "message": "Email not found."})

        otp = auth_service.generate_otp(email)
        print(otp)
        logger.debug(f"OTP {otp} sent to {email}")  # Log OTP for debugging

        return JsonResponse({"status": "success", "message": "OTP sent successfully."})
    


class VerifyOTPLoginView(View):
    def get(self,request):
        return render(request,'auth/signin.html')
    def post(self, request):
        email = request.POST.get("email")
        otp_entered = request.POST.get("otp")

        otp_stored = cache.get(f"otp_{email}")

        if not otp_stored or str(otp_entered) != str(otp_stored):
            return JsonResponse({"status": "error", "message": "Invalid or expired OTP."})

        # OTP is valid, create session
        request.session["email"] = email
        cache.delete(f"otp_{email}")  # Clear OTP after successful login

        return JsonResponse({"status": "success", "redirect": "/"})
    
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Destroy session
        return redirect("/api/verify-otp-login/")
