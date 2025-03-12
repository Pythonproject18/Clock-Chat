from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.auth import logout,login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..services import auth_service

@method_decorator(csrf_exempt, name='dispatch')
class OtpSendView(View):
    def post(self, request):
        email = request.POST.get("email")
        purpose = request.POST.get("purpose")  # Get purpose (signup or login)

        if not email or not purpose:
            return JsonResponse({"status": "error", "message": "Email and purpose are required"}, status=400)

        user_exists = auth_service.user_exists(email)

        if purpose == "login":
            if not user_exists:
                return JsonResponse({"status": "error", "message": "Email not found. Please sign up first."}, status=400)

        elif purpose == "signup":
            if user_exists:
                return JsonResponse({"status": "error", "message": "Email already exists. Please log in."}, status=400)

        else:
            return JsonResponse({"status": "error", "message": "Invalid purpose."}, status=400)

        # Generate OTP and store it
        otp = auth_service.generate_otp(email)
        cache.set(f"otp_{email}", otp, timeout=300)  # Store OTP for 5 minutes
        print(f"Your OTP for {email} is: {otp}")

        return JsonResponse({"status": "success", "message": f"OTP sent to {email}"}, status=200)


        return JsonResponse({"status": "success", "message": f"OTP sent to {email}"}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class OtpVerifyView(View):
    def post(self, request):
        email = request.POST.get("email")
        otp = request.POST.get("otp")

        if not email or not otp:
            return JsonResponse({"status": "error", "message": "Email and OTP are required"}, status=400)

        if str(cache.get(f"otp_{email}")) == str(otp):
            cache.set(f"verified_{email}", True, timeout=300)
            cache.delete(f"otp_{email}")
            return JsonResponse({"status": "success", "message": "OTP verified"}, status=200)

        return JsonResponse({"status": "error", "message": "Invalid OTP"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    def get(self, request):
        return render(request, 'auth/signup.html')

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        middle_name=request.POST.get("middle_name")
        email = request.POST.get("email")

        if not first_name or not last_name or not email:
            return JsonResponse({"status": "error", "message": "All fields are required"}, status=400)

        if not cache.get(f"verified_{email}"):
            return JsonResponse({"status": "error", "message": "OTP verification required"}, status=400)

        auth_service.create_user(first_name, middle_name, last_name, email)
        cache.delete(f"verified_{email}")
        return JsonResponse({"status": "success", "message": "User registered successfully", "redirect": "/sign-in/"})

class VerifyOTPLoginView(View):
    def get(self, request):
        return render(request, 'auth/signin.html')

    def post(self, request):
        email = request.POST.get("email")
        otp_entered = request.POST.get("otp")
        user = auth_service.get_user(email)  # Get user by email
        if str(cache.get(f"otp_{email}")) == str(otp_entered):
            login(request, user)  # Log in user
            request.session["email"] = user.email  # Store email in session
            cache.delete(f"otp_{email}")
            return JsonResponse({"status": "success", "redirect": "/"})

        return JsonResponse({"status": "error", "message": "Invalid or expired OTP."})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        return redirect("/api/verify-otp-login/")
