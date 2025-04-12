from CLOCK_CHAT.models import Message, User, Chat

def get_messages(chat_id):
    return Message.objects.filter(chat_id=chat_id, is_active=True).order_by('created_at')

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