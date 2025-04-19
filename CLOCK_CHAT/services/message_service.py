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

def create_message(text, chat_id, sender_id, created_by_id):
    try:
        # Get User and Chat instances
        sender = User.objects.get(id=sender_id)
        created_by = User.objects.get(id=created_by_id)
        chat = Chat.objects.get(id=chat_id)
        
        message = Message.objects.create(
            text=text,
            chat=chat,
            sender_id=sender,
            created_by=created_by,
            updated_by=created_by  # Assuming same user updates when creating
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
    

def get_message_reaction(message_id):
    reactions = MessageReaction.objects.filter(message = message_id,is_active = True).values('id','reaction')
    print(reactions)
    reaction_values = []
    if reaction_values:
        reaction_values.append = [
            {
                'id':reaction['id'],
                'value':get_reaction_value(reaction['id'])
            }
            for reaction in reactions
        ]


def get_reaction_value(reaction_id):
    reaction =Reaction.objects.filter(id = reaction_id,is_active = True).first()
    print(reaction)
    return reaction.value

