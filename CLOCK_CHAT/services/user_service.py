from CLOCK_CHAT.models import ChatMember, Chat, User, Chat_Type
from CLOCK_CHAT.services import chat_service
from CLOCK_CHAT.constants.default_values import Gender
import os
import hashlib
from django.conf import settings

def get_user_chats(user_id):
    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids, is_active=True).order_by('id')  # Ensures order 1-4
    return chats

def get_chat_details(user_id):
    user = User.objects.get(id=user_id)
    print(user)
    chat_ids = ChatMember.objects.filter(member=user_id, is_active=True).values_list('chat', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids).order_by('-created_at')

    chat_list = []
    for chat in chats:
        
        if chat.type == Chat_Type.PERSONAL.value:
            other_members = ChatMember.objects.filter(chat=chat, is_active=True).exclude(member=user)
            if other_members.exists():
                member = User.objects.get(id=other_members[0].member_id)
                title = f"{member.first_name} {member.middle_name} {member.last_name}"
            else:
                title = "Unknown"
            chat_type = Chat_Type(chat.type).name
        else:
            if chat.chat_title:
                title = chat.chat_title
            else:
                members = ChatMember.objects.filter(chat=chat, is_active=True)
                member_names = []
                for m in members:
                    user = User.objects.get(id=m.member_id)
                    member_names.append(f"{user.first_name} {user.middle_name} {user.last_name}")
                title = ", ".join(member_names) 
            chat_type = Chat_Type(chat.type).name

        member_count = ChatMember.objects.filter(chat=chat, is_active=True).count()
        creator = User.objects.get(id=chat.created_by_id)
        creator_name = f"{creator.first_name} {creator.middle_name} {creator.last_name}"

        members = ChatMember.objects.filter(chat=chat, is_active=True)
        member_details = []
        for member in members:
            user = User.objects.get(id=member.member_id)
            member_details.append({
                "user_id": user.id,
                "name": f"{user.first_name} {user.middle_name} {user.last_name}",
                "email": user.email,
            })
        
        chat_list.append({
            "id": chat.id,
            "title": title,
            "type": chat_type,
            "member_count": member_count,
            "created_by": creator_name,
            "members": member_details,
            'created_at':chat_service.global_timestamp(chat.created_at), 
        })
    
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