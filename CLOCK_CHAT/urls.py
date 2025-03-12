from django.urls import path
from . import views

urlpatterns = [
    # Chat
    path('', views.ChatListView.as_view(), name='chat_list'),
    path('chat/search/api', views.ChatSearchView.as_view(), name='search_api'),
    path('chat/create/api', views.ChatCreateView.as_view(), name='search_api'),
    path('api/send-otp/', views.OtpSendView.as_view(), name='send_otp'),
    path('api/verify-otp/', views.OtpVerifyView.as_view(), name='verify_otp'),
    path('api/signup/',views.SignUpView.as_view(), name='signup'),
    path('api/verify-otp-login/',views.VerifyOTPLoginView.as_view(), name='sign_in'),
    path('api/login/send_otp/', views.OtpSendView.as_view(), name='login_otp_send'),
    path('logout/', views.UserLogoutView.as_view(), name='log_out'),

    
    # Admin
    path('admin/', views.AdminHomeView.as_view(), name='admin_home'),

]
