from CLOCK_CHAT.models import ChatMember, Chat, User, Chat_Type, Message, MessageReaction
from django.db.models import Max, Q
from CLOCK_CHAT.services import chat_service
from CLOCK_CHAT.constants.default_values import Gender
import os
import hashlib
from django.conf import settings
from itertools import chain

def get_user_chats(user_id):
    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids, is_active=True).order_by('id')  # Ensures order 1-4
    return chats


def get_chat_details(user_id):
    user = User.objects.get(id=user_id)
    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids, is_active=True).distinct()

    chat_list = []


    for chat in chats:
        latest_message = Message.objects.filter(chat=chat, is_active=True).order_by('-created_at').first()
        latest_reaction = MessageReaction.objects.filter(
            message__chat=chat,
            is_active=True
        ).select_related('reacted_by', 'reaction', 'message').order_by('-updated_at').first()

        latest_time = chat.created_at
        subtitle = ""

        if latest_message:
            latest_time = latest_message.created_at

        if latest_reaction and (not latest_message or latest_reaction.updated_at > latest_message.created_at):
            # ✅ Reaction is latest
            reacted_by = latest_reaction.reacted_by
            reacted_by_name = reacted_by.first_name if reacted_by.id != user_id else "You"
            emoji_icon = latest_reaction.reaction.value
            reacted_message = latest_reaction.message

            msg_text = reacted_message.text or "a Voice message"

            subtitle = f"{emoji_icon} Reacted by {reacted_by_name} to: \"{msg_text}\""
            latest_time = latest_reaction.updated_at

        elif latest_message:
            # ✅ Message is latest
            if latest_message.audio_url:
                subtitle = "🎤 Voice message"
            elif latest_message.text:
                subtitle = latest_message.text
            else:
                subtitle = "📎 Media"

            if chat.type != Chat_Type.PERSONAL.value:
                sender = latest_message.sender_id
                sender_name = sender.first_name if sender.id != user_id else "You"
                subtitle = f"{sender_name}: {subtitle}"
        else:
            subtitle = ""
        # Check if latest message is seen by all other active members
        seen_by_all = False
        if latest_message:
            active_members = ChatMember.objects.filter(chat=chat, is_active=True).exclude(member=latest_message.sender_id)
            member_ids = set(active_members.values_list('member_id', flat=True))
            seen_ids = set(latest_message.seen_by or [])
            seen_by_all = member_ids.issubset(seen_ids)

    # Count Unread messages
        unread_count = Message.objects.filter(
            chat=chat, is_active=True
        ).exclude(seen_by__contains=[user.id]).exclude(sender_id=user.id).count()

        if chat.type == Chat_Type.PERSONAL.value:
            other_members = ChatMember.objects.filter(chat=chat, is_active=True).exclude(member=user.id)
            if other_members.exists():
                member = User.objects.get(id=other_members[0].member_id ,is_active=True)
                title = f"{member.first_name} {member.middle_name} {member.last_name}".strip()
                if not subtitle:
                    subtitle = member.bio or ""
            else:
                title = "Unknown"
        else:
            title = chat.chat_title or ", ".join([
                User.objects.get(id=m.member_id,is_active=True).first_name
                for m in ChatMember.objects.filter(chat=chat, is_active=True)
            ])

        chat_list.append({
            "id": chat.id,
            "title": title,
            "type": Chat_Type(chat.type).name,
            "member_count": ChatMember.objects.filter(chat=chat, is_active=True).count(),
            "created_by": f"{User.objects.get(id=chat.created_by_id).first_name} {User.objects.get(id=chat.created_by_id).middle_name} {User.objects.get(id=chat.created_by_id).last_name}".strip(),
            "members": [
                {
                    "user_id": m.member_id,
                    "name": f"{User.objects.get(id=m.member_id).first_name} {User.objects.get(id=m.member_id).middle_name} {User.objects.get(id=m.member_id).last_name}".strip(),
                    "email": User.objects.get(id=m.member_id).email,
                }
                for m in ChatMember.objects.filter(chat=chat, is_active=True)
            ],
            "latest_time": latest_time,
            "latest_text": subtitle,
            "latest_message_sender_id":latest_message.sender_id.id if latest_message else '',
            "unread_count": unread_count,
            "created_at": chat_service.global_timestamp(latest_time),
            "seen_by_all":seen_by_all
        })


    chat_list.sort(key=lambda c: c['latest_time'], reverse=True)
    print(chat_list)
    return chat_list



def get_user_object(user_id):
    return User.objects.filter(id=user_id,is_active=True).first()    

def get_all_users(user_id):
    return list(User.objects.filter(is_active=True).exclude(id=user_id))


def get_user_details(user_id):
    user = User.objects.filter(id=user_id,is_active=True).first()
    user_data = {
        'id':user.id,
        'full_name':user.get_full_name(),
        'email':user.email,
        'dob':user.dob,
        'bio':user.bio,
        'gender':user.gender,
        'date_joined':user.date_joined.strftime('%d-%m-%Y'),
        'profile_photo':user.profile_photo_url if user.profile_photo_url else '/static/images/default_avatar.png',
    }
    return user_data

def update_profile_data(field, value, user):
    if field == "about":
        user.bio = value
    elif field == "phone":
        user.phone = value
    elif field == "dob":
        user.dob = value
    elif field == "gender":
        user.gender = int(value)
    user.save()
    return True


def update_profile_photo(user,photo):
    filename_hash = hashlib.md5(photo.read()).hexdigest()
    extension = os.path.splitext(photo.name)[1] or ".png"
    photo.seek(0)  # Reset file pointer

    # Desired custom path
    relative_path = f"static/all-Pictures/Status/{filename_hash}{extension}"
    full_path = os.path.join(settings.BASE_DIR, relative_path)

    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Save the file manually
    with open(full_path, "wb") as f:
        f.write(photo.read())
    user_obj = get_user_object(user.id)
    # Update user's profile photo path (relative to your static dir)
    user_obj.profile_photo_url = f"/{relative_path}"  # Save as URL path for frontend
    user_obj.save()

    return relative_path