from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from CLOCK_CHAT.services import status_service
from django.shortcuts import render

class StatusListView(View):  # Use LoginRequiredMixin
    def get(self, request, *args, **kwargs):
        user = request.user.id  # Get logged-in user
        print(user)

        # Fetch friends (assuming a Friend model with a many-to-many relation)
        friends = status_service.get_friends_by_user(user)
        user_status = status_service.get_user_status(user)
        # Fetch statuses of friends (logic needed)
        
        return render(request,'status/status.html', {"friends": friends,'user_status':user_status})  # Use appropriate template
    
 
class StatusCreateView(View):
    def get(self,request):
        return render(request,"status/status")    
    
    def post(self,request):
         return render(request,"status/status.html")    