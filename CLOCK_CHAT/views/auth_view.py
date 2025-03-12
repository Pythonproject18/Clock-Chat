from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.auth import logout,login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from CLOCK_CHAT.services import auth_service
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.packages.response import success_response,error_response

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
                return JsonResponse(error_response(ErrorMessage.E00003.value))

        elif purpose == "signup":
            if user_exists:
                return JsonResponse(error_response(ErrorMessage.E00002.value))

        else:
            return JsonResponse({"status": "error", "message": "Invalid purpose."}, status=400)

        # Generate OTP and store it
        otp = auth_service.generate_otp(email)
        cache.set(f"otp_{email}", otp, timeout=300)  # Store OTP for 5 minutes
        print(f"Your OTP for {email} is: {otp}")


        msg = f"An OTP has been sent to {email}. Please check your email." # custom OTP Success Message
        
        return JsonResponse(success_response(msg), status=200)
        

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
            return JsonResponse(success_response(SuccessMessage.S00004.value), status=200)

        return JsonResponse(error_response(ErrorMessage.E00006.value))

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
        return JsonResponse(success_response(SuccessMessage.S00004.value, redirect="/sign-in/"), status=200)
        

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
