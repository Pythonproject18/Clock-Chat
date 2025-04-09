from django.views import View
from django.shortcuts import redirect, render

class AdminChatListView(View):
    def get(self, request):
        return render(request, 'adminuser/chats/chats_list.html')
    

class AdminChatUpdateView(View):
    def get(self, request, chat_id):
        return render(request, 'adminuser/chats/chat_update.html')
        