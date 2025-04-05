from django.http import JsonResponse
from django.views import View
from ..models import Chat, ChatMember, User
from django.db.models import Q

class ChatSearchView(View):
    def get(self, request):
        search_query = request.GET.get('search', '').strip().lower()
        current_user = request.user

        # Get all chats the current user is a member of
        user_chats = Chat.objects.filter(chatmember__user=current_user).distinct()

        matching_chats = []

        for chat in user_chats:
            chat_info = {
                'id': str(chat.id),
                'type': chat.type,
                'title': '',
                'chat_cover': '',
            }

            if chat.type.lower() == 'personal':
                # Get the other person in the personal chat
                other_member = ChatMember.objects.filter(chat=chat).exclude(user=current_user).first()
                if not other_member:
                    continue  # Skip if no recipient found (invalid case)

                full_name = f"{other_member.user.first_name} {other_member.user.middle_name} {other_member.user.last_name}".strip().lower()
                if search_query in full_name:
                    chat_info['title'] = full_name.title()
                    chat_info['chat_cover'] = getattr(other_member.user, 'profile_photo_url', '') or '/static/default-avatar.png'
                    matching_chats.append(chat_info)

            else:
                # For group chats: match by chat title
                if search_query in (chat.title or "").lower():
                    chat_info['title'] = chat.title
                    chat_info['chat_cover'] = chat.chat_cover or '/static/default-group.png'
                    matching_chats.append(chat_info)

        if not matching_chats:
            return JsonResponse([], safe=False)

        return JsonResponse(matching_chats, safe=False)
