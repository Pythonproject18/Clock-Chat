from CLOCK_CHAT.models import Message, User, Chat,MessageReaction,Reaction
from CLOCK_CHAT.constants.default_values import Delete_Type
from CLOCK_CHAT.services import chat_service
import os
import uuid
from django.conf import settings


def get_messages(chat_id, user_id):
    messages = Message.objects.filter(chat_id=chat_id, is_active=True)

    # Exclude messages that are deleted for everyone
    messages = messages.exclude(del_type=Delete_Type.FOR_ALL.value)

    # Exclude messages that are deleted for me by this user
    messages = messages.exclude(
        del_type=Delete_Type.FOR_ME.value,
        del_by__contains=[user_id]
    )

    return messages.order_by('created_at')

def create_message(text, chat_id, sender_id, created_by_id, reply_for_message_id=None):
    try:
        sender = User.objects.get(id=sender_id)
        created_by = User.objects.get(id=created_by_id)
        chat = Chat.objects.get(id=chat_id)

        # Get the replied-to message if provided
        reply_to_message = None
        if reply_for_message_id:
            reply_to_message = Message.objects.filter(id=reply_for_message_id).first()

        message = Message.objects.create(
            text=text,
            chat=chat,
            sender_id=sender,
            created_by=created_by,
            updated_by=created_by,
            reply_for_message=reply_to_message  # ✅ set reply reference
        )
        return message
    except Exception as e:
        print(f"Error creating message: {e}")
        return None
def create_message(text, chat_id, sender_id, created_by_id, reply_for_message_id=None):
    try:
        sender = User.objects.get(id=sender_id)
        created_by = User.objects.get(id=created_by_id)
        chat = Chat.objects.get(id=chat_id)

        # Get the replied-to message if provided
        reply_to_message = None
        if reply_for_message_id:
            reply_to_message = Message.objects.filter(id=reply_for_message_id).first()

        message = Message.objects.create(
            text=text,
            chat=chat,
            sender_id=sender,
            created_by=created_by,
            updated_by=created_by,
            reply_for_message=reply_to_message  # ✅ set reply reference
        )
        return message
    except Exception as e:
        print(f"Error creating message: {e}")
        return None
def create_message(text, chat_id, sender_id, created_by_id, reply_for_message_id=None):
    try:
        sender = User.objects.get(id=sender_id)
        created_by = User.objects.get(id=created_by_id)
        chat = Chat.objects.get(id=chat_id)

        # Get the replied-to message if provided
        reply_to_message = None
        if reply_for_message_id:
            reply_to_message = Message.objects.filter(id=reply_for_message_id).first()

        message = Message.objects.create(
            text=text,
            chat=chat,
            sender_id=sender,
            created_by=created_by,
            updated_by=created_by,
            reply_for_message=reply_to_message  # ✅ set reply reference
        )
        return message
    except Exception as e:
        print(f"Error creating message: {e}")
        return None
def create_message(text, chat_id, sender_id, created_by_id, reply_for_message_id=None):
    try:
        sender = User.objects.get(id=sender_id)
        created_by = User.objects.get(id=created_by_id)
        chat = Chat.objects.get(id=chat_id)

        # Get the replied-to message if provided
        reply_to_message = None
        if reply_for_message_id:
            reply_to_message = Message.objects.filter(id=reply_for_message_id).first()

        message = Message.objects.create(
            text=text,
            chat=chat,
            sender_id=sender,
            created_by=created_by,
            updated_by=created_by,
            reply_for_message=reply_to_message  # ✅ set reply reference
        )
        return message
    except Exception as e:
        print(f"Error creating message: {e}")
        return None
def create_message(text, chat_id, sender_id, created_by_id, reply_for_message_id=None):
    try:
        sender = User.objects.get(id=sender_id)
        created_by = User.objects.get(id=created_by_id)
        chat = Chat.objects.get(id=chat_id)

        # Get the replied-to message if provided
        reply_to_message = None
        if reply_for_message_id:
            reply_to_message = Message.objects.filter(id=reply_for_message_id).first()

        message = Message.objects.create(
            text=text,
            chat=chat,
            sender_id=sender,
            created_by=created_by,
            updated_by=created_by,
            reply_for_message=reply_to_message  # ✅ set reply reference
        )
        return message
    except Exception as e:
        print(f"Error creating message: {e}")
        return None
def create_message(text, chat_id, sender_id, created_by_id, reply_for_message_id=None):
    try:
        sender = User.objects.get(id=sender_id)
        created_by = User.objects.get(id=created_by_id)
        chat = Chat.objects.get(id=chat_id)

        # Get the replied-to message if provided
        reply_to_message = None
        if reply_for_message_id:
            reply_to_message = Message.objects.filter(id=reply_for_message_id).first()

        message = Message.objects.create(
            text=text,
            chat=chat,
            sender_id=sender,
            created_by=created_by,
            updated_by=created_by,
            reply_for_message=reply_to_message  # ✅ set reply reference
        )
        return message
    except Exception as e:
        print(f"Error creating message: {e}")
        return None
def create_message(text, chat_id, sender_id, created_by_id, reply_for_message_id=None):
    try:
        sender = User.objects.get(id=sender_id)
        created_by = User.objects.get(id=created_by_id)
        chat = Chat.objects.get(id=chat_id)

        # Get the replied-to message if provided
        reply_to_message = None
        if reply_for_message_id:
            reply_to_message = Message.objects.filter(id=reply_for_message_id).first()

        message = Message.objects.create(
            text=text,
            chat=chat,
            sender_id=sender,
            created_by=created_by,
            updated_by=created_by,
            reply_for_message=reply_to_message  # ✅ set reply reference
        )
        return message
    except Exception as e:
        print(f"Error creating message: {e}")
        return None
def create_message(text, chat_id, sender_id, created_by_id, reply_for_message_id=None):
    try:
        sender = User.objects.get(id=sender_id)
        created_by = User.objects.get(id=created_by_id)
        chat = Chat.objects.get(id=chat_id)

        # Get the replied-to message if provided
        reply_to_message = None
        if reply_for_message_id:
            reply_to_message = Message.objects.filter(id=reply_for_message_id).first()

        message = Message.objects.create(
            text=text,
            chat=chat,
            sender_id=sender,
            created_by=created_by,
            updated_by=created_by,
            reply_for_message=reply_to_message  # ✅ set reply reference
        )
        return message
    except Exception as e:
        print(f"Error creating message: {e}")
        return None


    
    
def update_message(message_id, text, updated_by_id):
    try:
        message = Message.objects.get(id=message_id)
        updated_by = User.objects.get(id=updated_by_id)
        
        message.text = text
        message.updated_by = updated_by
        message.is_edited = True
        message.save()
        return message
    except Message.DoesNotExist:
        return None
    except Exception as e:
        print(f"Error updating message: {e}")
        return None
    

# Add this new function for hard delete
def delete_message(message_id, purpose, user):
    try:
        print("delete function")
        message = get_message_object(message_id, user.id)
        print(message)

        message.created_by = User.objects.filter(id = user.id ,is_active=True).first()  # optional tracking
        print("created_by")
        if purpose == "delete for me":
            print("delete for me")
            message.del_type = Delete_Type.FOR_ME.value
            if user not in message.del_by:
                message.del_by.append(user.id)
        elif purpose == "delete for everyone":
            print("delete for all")

            message.del_type = Delete_Type.FOR_ALL.value
            message.is_active = False
        else:
            return False
        message.save()
        return True
    except Message.DoesNotExist:
        return False
    except Exception as e:
        print(f"Error deleting message: {e}")
        return False

    
def get_message_object(message_id,user_id):
    return Message.objects.filter(id = message_id,sender_id=user_id,is_active=True).first()



def voice_message_create(audio_file, chat_id, sender):
    # Generate unique filename
    filename = f"{uuid.uuid4().hex}.webm"
    relative_path = os.path.join('static', 'audio', filename)
    full_path = os.path.join(settings.BASE_DIR, relative_path)

    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Save file manually
    with open(full_path, 'wb') as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    # Audio URL to be served statically
    audio_url = f"/static/audio/{filename}"

    # Get chat object and save message
    chat = chat_service.get_chat_object(chat_id)
    return Message.objects.create(
        chat=chat,
        sender_id=sender,
        created_by=sender,
        updated_by=sender,
        audio_url=audio_url
    )

def react_to_message(message_id, emoji_class, user_id):
    try:
        message = Message.objects.get(id=message_id, is_active=True)
        reactions = message.emoji_reactions or {}

        # Remove user from all emojis first
        for icon in list(reactions.keys()):
            if user_id in reactions[icon]:
                reactions[icon].remove(user_id)
                # Clean up empty emoji lists
                if not reactions[icon]:
                    del reactions[icon]

        # If user had already selected this emoji, we treated it as a toggle (removed)
        # If not, now add it
        if emoji_class not in reactions or user_id not in reactions.get(emoji_class, []):
            reactions.setdefault(emoji_class, []).append(user_id)

        message.emoji_reactions = reactions
        message.save()
        return True
    except Message.DoesNotExist:
        return False
    
def create_media_messages(chat_id, user, files):
    saved_paths = []

    for key in files:
        file_list = files.getlist(key)
        for file in file_list:
            ext = os.path.splitext(file.name)[1]
            unique_name = f"{uuid.uuid4().hex}{ext}"
            save_path = os.path.join(settings.BASE_DIR, "static", "all-Pictures", "media", unique_name)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            saved_paths.append(f"/static/all-Pictures/media/{unique_name}")

    if not saved_paths:
        raise Exception("No valid media files found")

    return Message.objects.create(
        media_url=saved_paths,  # use updated field
        chat=chat_service.get_chat_object(chat_id),
        sender_id=user,
        created_by=user,
        updated_by=user  # this is required since model needs updated_by
    )