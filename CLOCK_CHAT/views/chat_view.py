from django.views import View
from django.shortcuts import render
from django.http import JsonResponse 
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required,auth_required
from django.contrib import messages
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.services import user_service


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')

class ChatListView(View):
    def get(self, request):
        user_id = request.user.id

        all_chats = user_service.get_chat_details(user_id)

        return render(request, 'enduser/Chats/test.html', {'chats': all_chats})


class ChatSearchView(View):
    def get(self, request):
        search_query = request.GET.get('q', '')
        
        return JsonResponse({"results": []}) 

class ChatCreateView(View):
    def get(self, request):
       
        return render(request, 'enduser/Chats/create_chat.html')

    def post(self, request):
      
        chat_name = request.POST.get('chat_name')

        return JsonResponse({"status": "success", "message": "Chat created successfully"})