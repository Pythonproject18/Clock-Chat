from datetime import datetime, timedelta
import pytz
from CLOCK_CHAT.models import Chat,ChatMember,Friend,User
from CLOCK_CHAT.constants.default_values import Chat_Type
from django.db.models import Count
import calendar
from django.utils import timezone
from django.db.models.functions import ExtractMonth


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
        type=Chat_Type.PERSONAL.value,
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
        type=Chat_Type.PERSONAL.value,
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


def create_group_chat_with_friend(current_user_id, user_ids):

    # Ensure at least 2 members + current user = group
    if len(user_ids) < 2:
        return None
    # Create new group chat
    chat = Chat.objects.create(
        type=Chat_Type.GROUP.value,
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



def get_chat_object(chat_id):
    return Chat.objects.filter(id=chat_id,is_active = True).first()


def get_chat_by_monthly_report():
    current_year = timezone.now().year

    # PERSONAL chats
    qs_personal = (
        Chat.objects
        .filter(
            type=Chat_Type.PERSONAL.value,
            is_active=True,
            created_at__year=current_year
        )
        .annotate(month=ExtractMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    counts_personal = {entry['month']: entry['count'] for entry in qs_personal}

    # GROUP chats
    qs_group = (
        Chat.objects
        .filter(
            type=Chat_Type.GROUP.value,
            is_active=True,
            created_at__year=current_year
        )
        .annotate(month=ExtractMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    counts_group = {entry['month']: entry['count'] for entry in qs_group}

    # Build full 12‑month skeleton
    labels = []
    data_personal = []
    data_group = []
    
    for m in range(1, 13):
        labels.append(calendar.month_abbr[m])
        data_personal.append(counts_personal.get(m, 0))
        data_group.append(counts_group.get(m, 0))

    return labels, data_personal, data_group