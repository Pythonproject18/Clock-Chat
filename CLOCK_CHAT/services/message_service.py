from CLOCK_CHAT.models import Message, User, Chat
from CLOCK_CHAT.constants.default_values import Delete_Type

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
