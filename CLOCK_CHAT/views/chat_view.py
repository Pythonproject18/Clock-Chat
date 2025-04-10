from django.views import View
from django.shortcuts import render,redirect
from django.http import JsonResponse 
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required,auth_required
from django.contrib import messages
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.services import user_service, message_service
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
      
        chat_name = request.POST.get('chat_name')

        return JsonResponse({"status": "success", "message": "Chat created successfully"})
    

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
        print("helloooo")
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

        


class MessageUpdateView(View):

    def post(self,request,message_id):

        return redirect("/message/")