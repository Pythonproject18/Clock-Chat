from django.http import JsonResponse
from django.views import View
from . import chat_service
from ..models import Chat

class ChatListViewApi(View):
    def get(self, request):
        user = request.user
        chats = chat_service.list_chats_by_user_api(user)  # Fetch all user chats
        chat_data_list = []

        # Build chat data list first
        for chat in chats:
            chat_info = {
                'id': chat.id,
                'title': '',
                'chat_cover': '',
            }
                # Personal chat
            if chat.type == Chat.PERSONAL.value:
                member = chat_service.get_recipient_for_personal(chat.id, user)
                chat_info['title'] = f"{member.first_name} {member.middle_name} {member.last_name}"
                chat_info['chat_cover'] = member.profile_photo_url # or '/static/images/avatar.jpg'
            else:  # Group chat
                chat_info['title'] = chat.title or chat_service.get_recipients_for_group(chat.id, user)
                chat_info['chat_cover'] = chat.chat_cover # or '/static/images/group_pic.png'

            chat_data_list.append(chat_info)

        # Apply filtering after the list is built
        filtered_chats = self.list_chats_api(request, chat_data_list)

        return JsonResponse(filtered_chats, safe=False)

    def list_chats_api(self, request, chat_data_list):
        """Filters the chat list based on a search query."""
        search_query = request.GET.get('search', '').strip().lower()

        if search_query:
            filtered_chats = [
                chat for chat in chat_data_list if search_query in chat['title'].lower()
            ]
        else:
            filtered_chats = chat_data_list  # Return full list if no search query

        return filtered_chats
