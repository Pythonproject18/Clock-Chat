from django.views import View
from django.shortcuts import render
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

        all_chats = user_service.get_chat_details(user_id)

        return render(request, 'enduser/Chats/chat.html', {'chats': all_chats})



@auth_required
@role_required(Role.END_USER.value, page_type='enduser')

class ChatSearchView(View):
    def get(self, request):
        search_query = request.GET.get('q', '')
        
        return JsonResponse({"results": []}) 


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')

class ChatCreateView(View):
    def get(self, request):
       
        return render(request, 'enduser/Chats/create_chat.html')

    def post(self, request):
      
        chat_name = request.POST.get('chat_name')

        return JsonResponse({"status": "success", "message": "Chat created successfully"})
    

# @auth_required
# @role_required(Role.END_USER.value, page_type='enduser')

# class MessageListView(View):
#     def get(self, request):
#         return render(request, 'enduser/Chats/message.html')

@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class MessageListView(View):
    def get(self, request):
        chat_id = request.GET.get('chat_id')
        if not chat_id:
            return JsonResponse({'status': 'error', 'message': 'Chat ID is required'}, status=400)
            
        messages = message_service.get_messages(chat_id)
        return render(request, 'enduser/Chats/message.html', {
            'messages': messages,
            'chat_id': chat_id,
            'request': request  # Pass request to template
        })
    
    def post(self, request):
        try:
            chat_id = request.POST.get('chat_id')
            message_text = request.POST.get('message_text')
            
            if not chat_id or not message_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Both chat_id and message_text are required'
                }, status=400)
                
            # Create message using the service layer
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