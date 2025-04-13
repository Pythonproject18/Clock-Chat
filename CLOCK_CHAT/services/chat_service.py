from datetime import datetime, timedelta
import pytz
from CLOCK_CHAT.models import Chat,ChatMember,Friend,User
from CLOCK_CHAT.constants.default_values import Chat_Type

def global_timestamp(timestamp):
    # Get current time in the same timezone as timestamp
    now = datetime.now(timestamp.tzinfo)

    diff = now - timestamp

    if diff < timedelta(days=1) and now.date() == timestamp.date():
        return f"{timestamp.strftime('%I:%M %p')}"
    elif diff < timedelta(days=2) and (now.date() - timestamp.date()).days == 1:
        return "Yesterday"
    elif diff < timedelta(days=7):
        return f"{timestamp.strftime('%A')}"
    else:
        return timestamp.strftime('%d-%m-%Y')


def create_friend_and_personal_chat(current_user_id, user_ids):
    if len(user_ids) != 1:
        return None

    friend_user_id = user_ids[0]

    # ✅ Check if a personal chat between the two already exists
    existing_chat = Chat.objects.filter(
        type=Chat_Type.Personal.value,
        fk_chat_cmember_chats_id__member=current_user_id
    ).filter(
        fk_chat_cmember_chats_id__member=friend_user_id
    ).distinct().first()

    if existing_chat:
        return existing_chat

    # ✅ Create mutual friendship if not exists
    Friend.objects.get_or_create(
        user_id=current_user_id,
        friend_id=friend_user_id,
        defaults={'created_by_id': current_user_id}
    )
    Friend.objects.get_or_create(
        user_id=friend_user_id,
        friend_id=current_user_id,
        defaults={'created_by_id': current_user_id}
    )

    # ✅ Create new personal chat
    chat = Chat.objects.create(
        type=Chat_Type.Personal.value,
        created_by_id=current_user_id,
    )

    # ✅ Add both users to ChatMember
    ChatMember.objects.create(
        chat_id=chat.id,
        member_id=current_user_id,
        created_by_id=current_user_id,
        is_admin=True
    )
    ChatMember.objects.create(
        chat_id=chat.id,
        member_id=friend_user_id,
        created_by_id=current_user_id,
        is_admin=False
    )

    return chat


def create_group_chat_with_friend(current_user_id, user_ids, chat_name="New Group"):
    from django.db.models import Count

    # Ensure at least 2 members + current user = group
    if len(user_ids) < 2:
        return None

    all_member_ids = set(user_ids + [current_user_id])

    # Check if an exact group already exists with same members and same type
    existing_chats = Chat.objects.filter(
        type=Chat_Type.GROUP.value,
        fk_chat_cmember_chats_id__member__in=all_member_ids
    ).annotate(member_count=Count('fk_chat_cmember_chats_id')).filter(
        member_count=len(all_member_ids)
    ).distinct()

    for chat in existing_chats:
        chat_member_ids = set(
            ChatMember.objects.filter(chat=chat).values_list('member_id', flat=True)
        )
        if chat_member_ids == all_member_ids:
            return chat  # Group already exists

    # Create new group chat
    chat = Chat.objects.create(
        chat_title=chat_name,
        type=Chat_Type.Group.value,
        created_by_id=current_user_id
    )

    # Add current user (creator) as admin
    ChatMember.objects.create(
        chat_id=chat.id,
        member_id=current_user_id,
        created_by_id=current_user_id,
        is_admin=True
    )

    # Add other members
    for uid in user_ids:
        ChatMember.objects.create(
            chat_id=chat.id,
            member_id=uid,
            created_by_id=current_user_id,
            is_admin=False
        )

    return chat

