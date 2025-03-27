from CLOCK_CHAT.models import ChatMember, Chat

# def get_user_chats(user_id):
#     chat_id=ChatMember.objects.filter(member=user_id,is_active=True).values('chat').first()
#     chat_data = [] 
#     if chat_id:
#         print(chat_id)       
#         chat_data=Chat.objects.filter(id=chat_id["chat"]).first()
#         print(chat_data.chat_title)
#     return chat_data

# def get_all_user_chats(user_id):
#     chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
#     chat_data = Chat.objects.filter(id__in=chat_ids)
#     print(chat_ids)
    
#     # print(f"User {user_id} is in chats: {list(chat_ids)}")
    
#     for chat in chat_data:
#         # print(f"Chat : {chat_ids} - {chat.chat_title}")
        
#         print(f"Chat : {chat.chat_title}")
        
#     return chat_data

def get_user_chats(user_id):
    # Get all active chat IDs for the user
    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    
    # Fetch all chat objects in one query
    chats = Chat.objects.filter(id__in=chat_ids)
    
    # Print formatted chat information
    if chats.exists():
        print(f"\nActive Chats for User {user_id}:")
        for chat in chats:
            print(f"Chat Title: {chat.chat_title}")
            print(f"Chat ID: {chat.id}")
            print(f"Created at: {chat.created_at}")
    else:
        print(f"\nUser {user_id} has no active chats")
    
    return chats

def get_chat_details(user_id):
    chats = get_user_chats(user_id)
    chat_list = [
        {"id": chat.id, "title": chat.chat_title, "created_at": chat.created_at} for chat in chats
    ]
    return chat_list