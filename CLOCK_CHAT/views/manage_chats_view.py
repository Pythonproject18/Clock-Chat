from django.views import View
from django.shortcuts import redirect, render

class AdminChatListView(View):
    def get(self, request):
        return render(request, 'adminuser/chats/chats_list.html')
        