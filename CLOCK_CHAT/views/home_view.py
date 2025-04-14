from django.views import View
from django.shortcuts import redirect,render
from CLOCK_CHAT.services import user_service

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/chat/')
        return render(request, 'enduser/home/landing.html')
    
class UserProfileView(View):
    def get(self,request):
        user_id = request.user.id
        user_details=user_service.get_user_details(user_id)
        return
