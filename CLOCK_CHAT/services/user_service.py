from CLOCK_CHAT.models import ChatMember, Chat, User, Chat_Type


def get_user_chats(user_id):
    
    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids, is_active=True).order_by('-created_at')
    return chats


def get_chat_details(user_id):
    
    chats = get_user_chats(user_id)
    
    current_user = User.objects.get(id=user_id)
    current_user_name = f"{current_user.first_name} {current_user.last_name}"

    chats = Chat.objects.all().order_by('id')

    chat_list = []
    for chat in chats:
        
        title = chat.chat_title if chat.chat_title else "Empty"
        
        if chat.type == Chat_Type.Personal.value:
            chat_type = "Personal" 
        else:
            chat_type = "Group" 

        member_count = ChatMember.objects.filter(chat=chat, is_active=True).count()

        creator = User.objects.get(id=chat.created_by_id)
        creator_name = f"{creator.first_name} {creator.last_name}"

        members = ChatMember.objects.filter(chat=chat, is_active=True)
        member_details = []
        for member in members:
            user = User.objects.get(id=member.member_id)
            member_details.append({
                "user_id": user.id,
                "name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "is_admin": member.is_admin
            })

        print(f"Chat ID: {chat.id}")
        print(f"Chat Title: {title}")
        print(f"Chat Type: {chat_type}")
        print(f"Number of Members: {member_count}")
        print(f"Created By: {creator_name}")
        print(f"Created At: {chat.created_at}")
        print("Members:")
        for member in member_details:
            print(f"  - User ID: {member['user_id']}")
            print(f"    Name: {member['name']}")
            print(f"    Email: {member['email']}")
            print(f"    Is Admin: {member['is_admin']}")

        chat_list.append({
            "id": chat.id,
            "title": title,
            "created_at": chat.created_at,
            "type": chat_type,
            "member_count": member_count,
            "created_by": creator_name,
            "members": member_details 
        })
    
    return chat_list