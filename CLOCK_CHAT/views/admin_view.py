from django.views import View
from django.shortcuts import render

class AdminHomeView(View):
    def get(self, request):
        return render(request, 'adminuser/base.html')