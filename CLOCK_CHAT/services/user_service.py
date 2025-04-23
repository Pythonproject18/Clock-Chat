from CLOCK_CHAT.models import ChatMember, Chat, User, Chat_Type, Message
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
        latest_message = Message.objects.filter(chat=chat).order_by('-created_at').first()
        latest_time = latest_message.created_at if latest_message else chat.created_at

        # ✅ Determine subtitle content
        if latest_message:
            if latest_message.audio_url:
                duration = len(latest_message.audio_url)
                minutes = duration // 60
                seconds = duration % 60
                formatted_duration = f"{minutes}:{seconds:02d}"
                subtitle = f"🎤 Voice message - {formatted_duration}"
            elif latest_message.text:
                subtitle = latest_message.text
                subtitle = subtitle if len(subtitle) <= 20 else subtitle[:20] + "..."
            else:
                subtitle = "📎 Media"

           
        # If no message at all
        else:
            subtitle = ""

        # Determine title
        if chat.type == Chat_Type.PERSONAL.value:
            other_members = ChatMember.objects.filter(chat=chat, is_active=True).exclude(member=user.id)
            if other_members.exists():
                member = User.objects.get(id=other_members[0].member_id)
                title = f"{member.first_name} {member.middle_name} {member.last_name}".strip()
                if not subtitle:
                    subtitle = member.bio or ""
            else:
                title = "Unknown"
        else:
            if chat.chat_title:
                title = chat.chat_title
            else:
                members = ChatMember.objects.filter(chat=chat, is_active=True)
                member_names = [
                    f"{User.objects.get(id=m.member_id).first_name} {User.objects.get(id=m.member_id).middle_name} {User.objects.get(id=m.member_id).last_name}".strip()
                    for m in members
                ]
                title = ", ".join(member_names)

        member_count = ChatMember.objects.filter(chat=chat, is_active=True).count()
        creator = User.objects.get(id=chat.created_by_id)
        creator_name = f"{creator.first_name} {creator.middle_name} {creator.last_name}".strip()

        members = ChatMember.objects.filter(chat=chat, is_active=True)
        member_details = [
            {
                "user_id": m.member_id,
                "name": f"{User.objects.get(id=m.member_id).first_name} {User.objects.get(id=m.member_id).middle_name} {User.objects.get(id=m.member_id).last_name}".strip(),
                "email": User.objects.get(id=m.member_id).email,
            }
            for m in members
        ]

        chat_list.append({
            "id": chat.id,
            "title": title,
            "type": Chat_Type(chat.type).name,
            "member_count": member_count,
            "created_by": creator_name,
            "members": member_details,
            "latest_time": latest_time,
            "latest_text": subtitle,
            "created_at": chat_service.global_timestamp(latest_time),
        })

    chat_list.sort(key=lambda c: c['latest_time'], reverse=True)
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