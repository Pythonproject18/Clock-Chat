from django.views import View
from django.http import JsonResponse
from CLOCK_CHAT.services import status_service,user_service
from django.shortcuts import render,redirect
from CLOCK_CHAT.decorator import auth_required, role_required
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.packages.file_management import save_uploaded_file
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.models import Status,StatusViewer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import base64




@auth_required
@role_required(Role.END_USER.value, page_type='enduser')

class StatusListView(View):  # Use LoginRequiredMixin
    def get(self, request):
        user = request.user.id  # Get logged-in user
        print(user)
        user_obj = user_service.get_user_object(user)

        # Fetch friends (assuming a Friend model with a many-to-many relation)
        friends = status_service.get_friends_by_user(user)
        user_status = status_service.get_user_status(user)
        # Fetch statuses of friends (logic needed)
        print(user_status)
        return render(request,'status/status.html',
            {
            'friends': friends,
            'user_status':user_status,
            'user_profile':user_obj.profile_photo_url if user_obj.profile_photo_url else '/static/images/default_avatar.png',
            }
        )  # Use appropriate template
    


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class StatusCreateView(View):
    def post(self, request):
        try:
            image_base64 = request.POST.get("image_base64")
            status_type = request.POST.get("type")
            caption = request.POST.get("caption")  # Get the caption here
            user_id = request.user.id

            if not image_base64:
                return JsonResponse({'error': 'No image uploaded'}, status=400)

            format, imgstr = image_base64.split(';base64,')
            ext = format.split('/')[-1]
            filename = f"status_{uuid.uuid4().hex}.{ext}"
            file = ContentFile(base64.b64decode(imgstr), name=filename)

            # Save the status
            image_path = save_uploaded_file(file, 'Status')
            status = status_service.create_status(image_path, user_id, status_type,caption)

            return redirect('status_list')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class StatusPreviewView(View):
    def get(self, request):
        try:
            user_id = request.user.id
            user = user_service.get_user_object(user_id)

            return render(request, "status/preview.html", {
                'user_profile': user.profile_photo_url if user.profile_photo_url else '/static/images/default_avatar.png',
                'user_name': f"{user.first_name} {user.middle_name} {user.last_name}"
            })
        except Exception as e:
            return render(request, "status/preview.html", {"error": str(e)})


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class StatusDetailView(View):
    def get(self, request, user_id):
        print(user_id)
        statuses = status_service.get_all_status_by_user_id(user_id)
        print(statuses)
        if not statuses.exists():
            return JsonResponse({'message': 'No status found'}, status=404)

        user = user_service.get_user_object(user_id)
        user_details = []

        if not user:
            return render(request, "status/status_view.html")

        user_details = {
            'id': user.id,
            'full_name': f"{user.first_name} {user.last_name}",
            'user_profile': user.profile_photo_url if user.profile_photo_url else '/static/images/default_avatar.png' ,
        }
        print(user_details)

        status_list = []
        for status in statuses:
            viewers = StatusViewer.objects.filter(status=status).select_related('viewed_by')
            viewer_list = [
                {
                    'id': viewer.id,
                    'viewed_by': viewer.viewed_by.username, 
                    'viewed_at': viewer.created_at
                }
                for viewer in viewers
            ]

            status_list.append({
                'id': status.id,
                'media_url': status.status_media if status.status_media else None,
                'caption':status.caption,
                'created_at': status.created_at,
                'type': status.status_type,
                'viewers': viewer_list  # Sending viewer list as JSON
            })
            print(status_list)

        return render(request, "status/status_view.html", {'status_details': status_list,'user_details':user_details})
