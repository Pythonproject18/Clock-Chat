from django.views import View
from django.shortcuts import render
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required, auth_required
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.packages.response import success_response, error_response

@auth_required
@role_required(Role.ADMIN.value, page_type='admin')
class AdminHomeView(View):
    def get(self, request):
        return render(request, 'adminuser/base.html')
    