from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from CLOCK_CHAT.services import status_service
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

class StatusListView(View):  # Use LoginRequiredMixin
    def get(self, request, *args, **kwargs):
        user = request.user.id  # Get logged-in user
        print(user)

        # Fetch friends (assuming a Friend model with a many-to-many relation)
        friends = status_service.get_friends_by_user(user)
        user_status = status_service.get_user_status(user)
        # Fetch statuses of friends (logic needed)
        
        return render(request,'status/status.html', {"friends": friends,'user_status':user_status})  # Use appropriate template
    
 
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class StatusCreateView(View):
    def get(self, request):
        return render(request, "status/status_create.html")

    def post(self, request):
        try:
            image = request.FILES.get('image')  # File object
            status_type = request.POST.get('type')
            user_id = request.user.id

            if not image:
                return JsonResponse({'error': 'No image uploaded'}, status=400)

            # Save the image to media storage
            status = status_service.create_status(image,user_id,status_type)
            return JsonResponse({'message': 'Status posted successfully!', 'id': status.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
