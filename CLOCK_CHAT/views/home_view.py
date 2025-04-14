from django.views import View
from django.shortcuts import redirect,render

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/chat/')
        return render(request, 'enduser/home/landing.html')
    
