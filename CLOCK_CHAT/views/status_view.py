from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from CLOCK_CHAT.services import status_service

@login_required
class StatusListView(View):
    
    def get(self, request, *args, **kwargs):
        user = request.user.id  # Get logged-in user
        print(user)
        # Fetch friends (assuming a Friend model with a many-to-many relation)
        friends = status_service.get_friends_by_user(user)

        # Fetch statuses of friends
       
        
        return