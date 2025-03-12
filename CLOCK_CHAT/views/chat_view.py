from django.views import View
from django.shortcuts import render


class ChatListView(View):
    def get(self, request):
        return render(request, 'enduser/Chats/test.html')
class ChatSearchView(View):
    def get(self,request):
        return
    
class ChatCreateView(View):
    def get(self,request):
        return
    
    def post(self,request):
        return