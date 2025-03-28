from django.views import View
from django.http import JsonResponse
from CLOCK_CHAT.services import status_service
from django.shortcuts import render
from CLOCK_CHAT.decorator import auth_required, role_required
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.packages.file_management import save_uploaded_file
from django.contrib import messages
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage



@auth_required
@role_required(Role.END_USER.value, page_type='enduser')

class StatusListView(View):  # Use LoginRequiredMixin
    def get(self, request):
        user = request.user.id  # Get logged-in user
        print(user)

        # Fetch friends (assuming a Friend model with a many-to-many relation)
        friends = status_service.get_friends_by_user(user)
        user_status = status_service.get_user_status(user)
        # Fetch statuses of friends (logic needed)
        
        return render(request,'status/status.html', {"friends": friends,'user_status':user_status})  # Use appropriate template
    


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')

class StatusCreateView(View):
    def get(self, request):
        return render(request, "status/status_create.html")

    def post(self, request):
        try:
            image = request.FILES.get('image')  # File object
            status_type = request.POST.get('type')
            user_id = request.user.id
            image_path = save_uploaded_file(image, 'Status')
            if not image:
                return JsonResponse({'error': 'No image uploaded'}, status=400)

            # Save the image to media storage
            status = status_service.create_status(image_path, user_id, status_type)
            return JsonResponse({'message': 'Status posted successfully!', 'id': status.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
