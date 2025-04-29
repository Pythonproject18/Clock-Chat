from django.views import View
from django.shortcuts import redirect, render
from CLOCK_CHAT.services import chat_service

class AdminChatListView(View):
    def get(self, request):
        chats = chat_service.get_all_chats()
        return render ( request ,'adminuser/chats/chats_list.html', {'chats': chats } )

class AdminChatUpdateView(View):
    def get(self, request, chat_id):
        return render(request, 'adminuser/chats/chat_update.html')
        