from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),

    # Admin
    path('admin/', views.AdminHomeView.as_view(), name='admin_home'),

    #chats
    path('chat/search/api', views.ChatSearchView.as_view(), name='search_api'),
    path('chat/create/api', views.ChatCreateView.as_view(), name='search_api'),
    path('api/send-otp/', views.OtpSendView.as_view(), name='send_otp'),
    path('api/verify-otp/', views.OtpVerifyView.as_view(), name='verify_otp'),
    path('api/signup/',views.SignUpView.as_view(), name='signup'),
    path('api/verify-otp-login/',views.VerifyOTPLoginView.as_view(), name='sign_in'),
    path('api/login/send_otp/', views.SendOTPView.as_view(), name='login_otp_send')

]
