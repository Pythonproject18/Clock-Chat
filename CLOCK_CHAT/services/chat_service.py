from ..models import Chat

def get_all_chats():
    return Chat.objects.all()

def get_chat_by_id(chat_id):
    return Chat.objects.get(id=chat_id)

def toggle_chat_status(chat_id, new_status):
    chat = Chat.objects.get(id=chat_id)
    chat.status = new_status
    chat.save()
    return chat

