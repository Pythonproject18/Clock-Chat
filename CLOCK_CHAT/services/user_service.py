from CLOCK_CHAT.models import ChatMember, Chat, User
from CLOCK_CHAT.constants.default_values import Chat_Type

def get_user_chats(user_id):
    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids).distinct()
    return chats


def get_chat_details(user_id):

    current_user = User.objects.get(id=user_id)
    current_user_name = f"{current_user.first_name} {current_user.last_name}"

    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids).order_by('id')

    chat_list = []
    for chat in chats:
        title = chat.chat_title if chat.chat_title else "Empty"
        
        if chat.type == Chat_Type.Personal.value:
            chat_type = current_user.first_name and current_user.first_name
        else:
            chat_type =  chat.chat_title

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

        print(f"Chat ID: {chat.id}")
        print(f"Chat Title: {title}")
        print(f"Chat Type: {chat_type}")
        print(f"Member: {member_count}")
        print(f"Created By: {creator_name}")
        print("Members:")
        for member in member_details:
            print(f"  - User ID: {member['user_id']}")
            print(f"    Name: {member['name']}")
            print(f"    Email: {member['email']}")

        chat_list.append({
            "id": chat.id,
            "title": title,
            "type": chat_type,
            "member_count": member_count,
            "created_by": creator_name,
            "members": member_details 
        })
    
    return chat_list