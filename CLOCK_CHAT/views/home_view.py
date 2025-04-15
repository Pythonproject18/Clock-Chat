from django.views import View
from django.shortcuts import redirect,render
from CLOCK_CHAT.services import user_service
from django.http.response import JsonResponse
import json

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/chat/')
        return render(request, 'enduser/home/landing.html')
    
class UserProfileView(View):
    def get(self, request):
        user_id = request.user.id
        user_details = user_service.get_user_details(user_id)
        print(user_details)
        return JsonResponse(user_details, safe=False)


class UserProfileUpdateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            field = data.get('field')
            value = data.get('value')

            user = request.user
            if not user.is_authenticated:
                return JsonResponse({'success': False, 'message': 'Not authenticated'}, status=403)
            print(value)
            update = user_service.update_profile_data(field,value,user)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)