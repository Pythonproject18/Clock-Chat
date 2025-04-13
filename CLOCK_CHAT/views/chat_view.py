from django.views import View
from django.shortcuts import render
from django.http import JsonResponse 
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required,auth_required
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.services import user_service,chat_service
import json


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class ChatListView(View):
    def get(self, request):
        user_id = request.user.id
        users = user_service.get_all_users()
        user_details = []

        if users:
            user_details = [
                {
                    'id': user.id,
                    'profile_pic': user.profile_photo_url if user.profile_photo_url else '/static/images/default_avatar.png',
                    'full_name':f"{user.first_name}{user.last_name}",
                }
                for user in users
            ]
        all_chats = user_service.get_chat_details(user_id)
        return render(request, 'enduser/Chats/chat.html', {'chats': all_chats,'users':user_details})


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class ChatCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_ids = data.get("user_ids", [])
        chat_name = data.get("chat_name", "")
        print(data)
        current_user_id = request.user.id

        if len(user_ids) == 1:
            chat = chat_service.create_friend_and_personal_chat(current_user_id, user_ids)
            print("chat",chat)
        else:
            chat = chat_service.create_group_chat_with_friend(current_user_id, user_ids, chat_name)

        if chat:
            return JsonResponse({"status": "success", "chat_id": chat.id})
        else:
            return JsonResponse({"status": "error", "message": "Chat creation failed"}, status=400)
