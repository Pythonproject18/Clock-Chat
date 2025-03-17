from django.views import View
from django.shortcuts import render, redirect
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required, auth_required
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.packages.response import success_response, error_response
from django.contrib import messages  # For user feedback
from django.contrib.auth import authenticate, login, logout


class LoginAdminView(View):
    def get(self, request):
        return render(request, 'adminuser/admin_login/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        otp = request.POST.get('otp')  # corrected field name

        # Authenticate the user. Adjust keyword if you're using email as username.
        user = authenticate(request, username=email, otp=otp)
        if user is not None:
            if user.roles in (Role.ADMIN.value, Role.SUPER_ADMIN.value):
                login(request, user)
                messages.success(request, SuccessMessage.S00001.value)
                return redirect('admin_home')  # Redirect to your admin home view; using named URL
                
            else:
                messages.error(request, ErrorMessage.E00001.value)
        else:
            messages.error(request, "Invalid email or password.")
        return redirect('login_myadmin')
    

class LoginOutAdminView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Destroy session
        return redirect("/login/admin/")



@auth_required( login_url='/login/admin/')
@role_required(Role.ADMIN.value, page_type='admin')
class AdminHomeView(View):
    def get(self, request):
        return render(request, 'adminuser/base.html')
    
