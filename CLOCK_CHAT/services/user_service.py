from CLOCK_CHAT.models import ChatMember, Chat, User, Chat_Type

def get_user_chats(user_id):
    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids, is_active=True).order_by('id')  # Ensures order 1-4
    return chats

def get_chat_details(user_id):
    user = User.objects.get(id=user_id)
    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids).order_by('id')

    chat_list = []
    for chat in chats:
        
        if chat.type == Chat_Type.Personal.value:
            member = ChatMember.objects.filter(chat=chat, is_active=True).exclude(member=user).first().member
            title = f"{member.first_name} {member.last_name}"
            chat_type = "Personal"
        else:
            if chat.chat_title:
                title = chat.chat_title
            else:
                members = ChatMember.objects.filter(chat=chat, is_active=True)
                member_names = []
                for m in members:
                    user = User.objects.get(id=m.member_id)
                    member_names.append(f"{user.first_name} {user.last_name}")
                title = ", ".join(member_names) 
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
            })
        
        chat_list.append({
            "id": chat.id,
            "title": title,
            "type": chat_type,
            "member_count": member_count,
            "created_by": creator_name,
            "members": member_details 
        })
    
    return chat_list


def get_user_object(user_id):
    return User.objects.filter(id=user_id,is_active=True).first()    

def get_all_users():
    return list(User.objects.filter(is_active=True))
