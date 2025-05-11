from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from CLOCK_CHAT.services import status_service,user_service
from django.shortcuts import render,redirect
from CLOCK_CHAT.decorator import auth_required, role_required
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.packages.file_management import save_uploaded_file
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.models import Status,StatusViewer
from django.core.files.base import ContentFile
import uuid
import base64
from CLOCK_CHAT.constants.default_values import Status_Type
import json
from django.core.files.storage import default_storage


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')

class StatusListView(View):  # Use LoginRequiredMixin
    def get(self, request):
        user = request.user.id  # Get logged-in user
        user_obj = user_service.get_user_object(user)

        # Fetch friends (assuming a Friend model with a many-to-many relation)
        friends = status_service.get_friends_by_user(user)
        user_status = status_service.get_user_status(user)
        # Fetch statuses of friends (logic needed)
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
            user_id = request.user.id
            content_type = request.META.get('CONTENT_TYPE', '')

            if 'application/json' in content_type:
                is_json = True
                # Handle JSON (text status)
                data = json.loads(request.body)
                base64_data = data.get("image") or data.get("image_base64")  # support both keys
                caption = data.get("caption", "")
            else:
                is_json = False
                # Handle form-data (photo/video status via base64)
                base64_data = request.POST.get("image") or request.POST.get("image_base64")
                caption = request.POST.get("caption", "")

            # Validate the base64 data
            if not base64_data or ';base64,' not in base64_data:
                return JsonResponse({'error': 'Invalid or missing base64 data'}, status=400)

            # Extract base64 content
            format, b64 = base64_data.split(';base64,')
            mime_type = format.split(':')[1]
            ext = mime_type.split('/')[-1]

            # Check if the file is of a valid type
            if ext not in ['png', 'jpg', 'jpeg', 'mp4', 'webm']:
                return JsonResponse({'error': 'Unsupported file type'}, status=400)

            # Check if the base64 data is too large
            if len(b64) > (50 * 1024 * 1024):  # 50MB limit
                return JsonResponse({'error': 'File size exceeds the 50MB limit'}, status=400)

            # Decode the base64 data
            file = ContentFile(base64.b64decode(b64), name=f"status_{uuid.uuid4().hex}.{ext}")

            # Save file to the desired location
            file_path = save_uploaded_file(file, 'Status')

            # Determine the status type (image, video, etc.)
            if mime_type.startswith('video'):
                status_type = Status_Type.VIDEO.value
            elif mime_type.startswith('image'):
                status_type = Status_Type.IMAGE.value
            else:
                status_type = Status_Type.TEXT.value

            # Create the status in the database
            status_service.create_status(file_path, user_id, status_type, caption)

            # Return appropriate response
            if is_json:
                return JsonResponse({'message': 'Status saved successfully', 'redirect_url': '/status/'})
            else:
                return HttpResponseRedirect('/status/')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Handle unexpected errors@auth_required
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

    def post(self, request):
        if request.method == 'POST' and request.FILES['file']:
            uploaded_file = request.FILES['file']
            
            # Check the file size (e.g., 20MB limit)
            max_size = 20 * 1024 * 1024  # 20MB in bytes
            if uploaded_file.size > max_size:
                return JsonResponse({'success': False, 'message': 'File size exceeds the limit.'})

            # Save the file to the default storage (temporary location)
            file_path = default_storage.save(f"status_preview/{uploaded_file.name}", ContentFile(uploaded_file.read()))
            
            # Get the URL to access the file
            file_url = default_storage.url(file_path)

            return JsonResponse({'success': True, 'url': file_url})

        return JsonResponse({'success': False, 'message': 'No file uploaded.'})

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
            print(status_list)

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

     

@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class StatusDeleteTempView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            file_path = data.get("file_path")
            if not file_path:
                return JsonResponse({"success": False, "message": "Missing file_path"}, status=400)
            print("going to delete")
            deleted = status_service.delete_temp_status_file()
            if deleted:
                return JsonResponse({"success": True, "message": "Temporary file deleted"})
            else:
                return JsonResponse({"success": False, "message": "File not found or could not be deleted"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
