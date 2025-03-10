from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),

    # Admin
    path('admin/', views.AdminHomeView.as_view(), name='admin_home'),
    
]
