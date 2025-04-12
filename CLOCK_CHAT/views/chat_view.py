from django.views import View
from django.shortcuts import render,redirect
from django.http import JsonResponse 
from CLOCK_CHAT.constants import Chat_Type
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required,auth_required
from django.contrib import messages
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.services import user_service, message_service
from CLOCK_CHAT.models import Chat, ChatMember, Friend, User, Message
import json
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
        try:
            data = json.loads(request.body)
            target_user_id = data.get('user_id')
            current_user = request.user

            if not target_user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            try:
                target_user = User.objects.get(id=target_user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Target user does not exist'}, status=404)

            # Create friendship both directions (if not exists)
            for user1, user2 in [(current_user, target_user), (target_user, current_user)]:
                Friend.objects.get_or_create(
                    user=user1,
                    friend=user2,
                    defaults={'created_by': current_user}
                )

            # Optional: Check if chat already exists
            existing_chat = Chat.objects.filter(
                type=Chat_Type.PERSONAL.value,
                members=current_user
            ).filter(members=target_user).first()

            if existing_chat:
                return JsonResponse({'chat_id': existing_chat.id, 'title': f"{target_user.first_name} {target_user.middle_name or ''} {target_user.last_name}".strip()})

            # Create new PERSONAL chat
            new_chat = Chat.objects.create(
                type=Chat_Type.PERSONAL.value,
                created_by=current_user,
                updated_by=current_user
            )

            # Add members
            for member, is_admin in [(current_user, True), (target_user, False)]:
                ChatMember.objects.create(
                    chat=new_chat,
                    member=member,
                    is_admin=is_admin,
                    created_by=current_user,
                    updated_by=current_user
                )

            return JsonResponse({'chat_id': new_chat.id, 'title': target_user.get_full_name()})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    

@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class MessageListView(View):
    def get(self, request,chat_id):
        if not chat_id:
            return JsonResponse({'status': 'error', 'message': 'Chat ID is required'}, status=400)

        messages = message_service.get_messages(chat_id)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return messages as JSON for AJAX
            messages_data = [
                {
                    'id': msg.id,
                    'text': msg.text,
                    'created_at': msg.created_at.strftime("%I:%M %p"),
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
            message = Message.objects.get(id=message_id, sender_id=request.user.id)
            
            deleted = message_service.delete_message(message_id)
            
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