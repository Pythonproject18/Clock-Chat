from django.views import View
from django.shortcuts import redirect,render

class HomeView(View):
    def get(self, request):
        return render(request, 'enduser/home/landing.html', )
    
