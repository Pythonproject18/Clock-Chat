from django.views import View
from django.shortcuts import render
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required,auth_required
from django.contrib import messages  # For user feedback
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage

@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class ChatListView(View):
    def get(self, request):
        messages.success(request, SuccessMessage.S00001.value)
        return render(request, 'enduser/Chats/test.html')


class ChatSearchView(View):
    def get(self,request):
        return


class ChatCreateView(View):
    def get(self,request):
        return
    
    def post(self,request):
        return