from django.views import View
from ..services import auth_service,user_service
from django.shortcuts import render, redirect
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required, auth_required
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.packages.response import success_response, error_response
from django.contrib import messages  # For user feedback
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import JsonResponse




class LoginAdminView(View):
    def get(self, request):
        return render(request, 'adminuser/admin_login/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        
        # Retrieve the stored OTP for this email
        stored_otp = cache.get(f"otp_{email}")
        if not stored_otp:
            return JsonResponse(error_response("OTP expired or not sent. Please request a new OTP."), status=400)
        
        # Compare the submitted OTP with the stored one
        if str(stored_otp) != str(otp):
            return JsonResponse(error_response("Invalid OTP. Please try again."), status=400)
        
        # OTP is valid; remove it from cache
        cache.delete(f"otp_{email}")
        
        try:
            # Retrieve the user using your auth service
            user = auth_service.get_user(email=email)
        except user.DoesNotExist:
            return JsonResponse(error_response("User does not exist."), status=400)
        
        # Verify that the user has admin or super-admin privileges
        if user.role == Role.ADMIN.value:
            login(request, user)
            return JsonResponse(success_response(SuccessMessage.S00004.value, redirect="/admin/"), status=200)
        else:
            return JsonResponse(error_response(ErrorMessage.E00001.value), status=400)



    

class LoginOutAdminView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Destroy session
        return redirect("/login/admin/")



@auth_required( login_url='/login/admin/')
@role_required(Role.ADMIN.value, page_type='admin')
class AdminHomeView(View):
    def get(self, request):
        return render(request, 'adminuser/dashboard.html')
    
