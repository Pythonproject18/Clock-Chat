from django.views import View
from django.shortcuts import render
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required,auth_required

class ChatListView(View):
    @role_required(Role.END_USER.value, page_type='enduser')
    @auth_required
    def get(self, request):
        print("Session Data:", request.session.items())  # ✅ Debug session
        print("User:", request.user)
        print("Is Authenticated:", request.user.is_authenticated)
        return render(request, 'enduser/Chats/test.html')
class ChatSearchView(View):
    def get(self,request):
        return
    
class ChatCreateView(View):
    def get(self,request):
        return
    
    def post(self,request):
        return