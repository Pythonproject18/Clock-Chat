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
import json
from CLOCK_CHAT.constants.default_values import Status_Type




@auth_required
@role_required(Role.END_USER.value, page_type='enduser')

class StatusListView(View):  # Use LoginRequiredMixin
    def get(self, request):
        print("gbhjbjhjhbhbhgbhjbjhbhbjhjjnj")
        user = request.user.id  # Get logged-in user
        user_obj = user_service.get_user_object(user)

        # Fetch friends (assuming a Friend model with a many-to-many relation)
        friends = status_service.get_friends_by_user(user)
        user_status = status_service.get_user_status(user)
        # Fetch statuses of friends (logic needed)
        print("data",friends)
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
        statuses = status_service.get_all_status_by_user_id(user_id)
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
        status_list = []
        for status in statuses:
            if request.user.id != user.id:  # don't count view for own status
                exists = StatusViewer.objects.filter(status=status, viewed_by=request.user).exists()
                if not exists:
                    status_service.status_viewer_create(status,request.user,user)

            status_list.append({
                'id': status.id,
                'media_url': status.status_media if status.status_media else None,
                'caption':status.caption,
                'created_at': status.created_at,
                'type': status.status_type,
                'viewers_count': status_service.get_status_viewers_count(status.id,user_id),  # Sending viewer list as JSON
            })
            # print(status_list)

        return render(request, "status/status_view.html", {'status_details': status_list,'user_details':user_details})




@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class GetStatusViewersView(View):
    def get(self, request, status_id):
        try:
            viewers = status_service.get_status_viewer(status_id)
            data = []
            for viewer in viewers:
                user = user_service.get_user_object(viewer['viewed_by'])  # corrected
                data.append({
                    'id': user.id,
                    'full_name': f"{user.first_name} {user.middle_name} {user.last_name}".strip(),
                    'profile_pic': user.profile_photo_url if user.profile_photo_url else '/static/images/default_avatar.png'
                })
            return JsonResponse({'viewers': data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class TextStatusCreateView(View):
     def get(self, request):
        try:
            user_id = request.user.id
            user = user_service.get_user_object(user_id)

            return render(request, "status/text_status.html", {
                'user_profile': user.profile_photo_url if user.profile_photo_url else '/static/images/default_avatar.png',
                'user_name': f"{user.first_name} {user.middle_name} {user.last_name}"
            })
        except Exception as e:
            return render(request, "status/text_status.html", {"error": str(e)})

     def post(self, request):
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Extract values from the request body
            text = data.get('text', '').strip()
            background_color = data.get('background_color', '')
            status_type = Status_Type.TEXT.value

            if not text:
                return JsonResponse({"error": "Text cannot be empty."}, status=400)

            # Create and save the new Status object
            status = Status.objects.create(
                text=text,
                background_color=background_color,
                status_type=status_type,
                created_by=request.user,  # Assuming `request.user` is the logged-in user
            )

            return JsonResponse({"message": "Status created successfully!", "status_id": status.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)