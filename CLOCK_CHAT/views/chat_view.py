from django.views import View
from django.shortcuts import render,redirect
from django.http import JsonResponse 
from CLOCK_CHAT.constants import Chat_Type
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required,auth_required
from django.contrib import messages
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.services import user_service, message_service,chat_service
import json
from CLOCK_CHAT.models import Message
# from CLOCK_CHAT.models import User


class HomeView(View):
    def get(self, request):
        return render(request, 'enduser/home/landing.html', )



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
@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class MessageListView(View):
    def get(self, request,chat_id):
        user_id=request.user.id
        if not chat_id:
            return JsonResponse({'status': 'error', 'message': 'Chat ID is required'}, status=400)

        messages = message_service.get_messages(chat_id,user_id)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return messages as JSON for AJAX
            messages_data = [
                {
                    'id': msg.id,
                    'text': msg.text,
                    'created_at': msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'sender_id': msg.sender_id.id,
                    'sender_name': f"{msg.sender_id.first_name} {msg.sender_id.last_name}"
                }
                for msg in messages
            ]
            return JsonResponse({
                'status': 'success',
                'chat_id': chat_id,
                'messages': messages_data
            })
class MessageCreateView(View):   
    def post(self, request, chat_id):
        try:
            message_text = request.POST.get('message_text')
            
            if not message_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'message_text is required'
                }, status=400)
                
            message = message_service.create_message(
                text=message_text,
                chat_id=chat_id,
                sender_id=request.user.id,
                created_by_id=request.user.id
            )
            
            if message:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Message sent successfully',
                    'data': {
                        'id': message.id,
                        'text': message.text,
                        'created_at': message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        'sender_id': message.sender_id.id,
                        'sender_name': f"{message.sender_id.first_name} {message.sender_id.last_name}"
                    }
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to create message'
            }, status=500)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

        


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class MessageUpdateView(View):
    def post(self, request, message_id):
        try:
            message_text = request.POST.get('message_text')
            chat_id = request.POST.get('chat_id')
            
            if not message_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'message_text is required'
                }, status=400)
                
            message = message_service.update_message(
                message_id=message_id,
                text=message_text,
                updated_by_id=request.user.id
            )
            
            if message:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Message updated successfully',
                    'data': {
                        'id': message.id,
                        'text': message.text,
                        'updated_at': message.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Message not found or you are not the sender'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
            
            
            
@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class MessageDeleteView(View):
    def post(self, request, message_id):
        try:
            data = json.loads(request.body)
            purpose = data.get('purpose')
            message = message_service.get_message_object(message_id, request.user.id)
            
            deleted = message_service.delete_message(message_id,purpose,request.user)
            
            if deleted:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Message deleted successfully'
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to delete message'
            }, status=500)
            
        except Message.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Message not found or you are not the sender'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)