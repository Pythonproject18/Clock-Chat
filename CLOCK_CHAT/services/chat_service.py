from ..models import Chat, ChatMember, User
from django.db.models import Q

def find_chats_with_user(current_user, target_username):
    try:
        target_user = User.objects.get(username=target_username)
    except User.DoesNotExist:
        return []

    # Find common chats
    common_chats = Chat.objects.filter(
        chatmember__user=current_user
    ).filter(
        chatmember__user=target_user
    ).distinct()

    return common_chats
