from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),



    # Authentication
    path('api/send-otp/', views.OtpSendView.as_view(), name='send_otp'),
    path('api/verify-otp/', views.OtpVerifyView.as_view(), name='verify_otp'),
    path('api/signup/', views.SignUpView.as_view(), name='signup'),
    path('api/verify-otp-login/', views.VerifyOTPLoginView.as_view(), name='sign_in'),
    path('api/login/send_otp/', views.OtpSendView.as_view(), name='login_otp_send'),
    path('logout/', views.UserLogoutView.as_view(), name='log_out'),

    
    # Admin
    path('login/admin/', views.LoginAdminView.as_view(), name='login_myadmin'),
    path('admin/log-out/', views.LoginOutAdminView.as_view(), name='logout_myadmin'),
    path('admin/', views.AdminHomeView.as_view(), name='admin_home'),

    # Admin Chats
    path('admin/chats/', views.AdminChatListView.as_view(), name='admin_chats_list'),
    path('admin/chats/<int:chat_id>/update/', views.AdminChatUpdateView.as_view(), name='admin_chat_update'),

    # Admin Profile
    path('admin/profile/', views.AdminProfileView.as_view(), name='admin_profile'),
    path('admin/profile/update/', views.AdminProfileUpdateView.as_view(), name='admin_profile_update'),
    
    

    # Chats
    path('chat/create/', views.ChatCreateView.as_view(), name='create'),
    path('chat/', views.ChatListView.as_view(), name='chat_list'),
    path('userprofile/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='user_profile_update'),

    

    # Status
    path('status/', views.StatusListView.as_view(), name='status_list'),
    path('status/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('status/<int:user_id>/',views.StatusDetailView.as_view(), name='status_detail'),
    path("status/preview/", views.StatusPreviewView.as_view(), name="status_preview"),
    path('status/viewers/<int:status_id>/', views.GetStatusViewersView.as_view(), name='status-viewers'),

    

    #message
    path('message/<int:chat_id>', views.MessageListView.as_view(), name="message"),
    path('message/create/<int:chat_id>', views.MessageCreateView.as_view(), name="message_create"),
    path('message/update/<int:message_id>', views.MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:message_id>', views.MessageDeleteView.as_view(), name='message_delete'),
    path('send-audio-message/', views.SendAudioMessageView.as_view(), name='audio_message_send'),
]