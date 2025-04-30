from django.views import View
from django.shortcuts import redirect,render
from CLOCK_CHAT.services import message_service, reactions_service
import json
from django.http.response import JsonResponse
from CLOCK_CHAT.constants.default_values import Role
from CLOCK_CHAT.decorator import role_required,auth_required
from CLOCK_CHAT.constants.error_message import ErrorMessage
from CLOCK_CHAT.constants.success_message import SuccessMessage
from CLOCK_CHAT.models import MessageReaction

@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class MessageListView(View):
    def get(self, request,chat_id):
        user_id=request.user.id
        if not chat_id:
            return JsonResponse({'status': 'error', 'message': 'Chat ID is required'}, status=400)

        messages = message_service.get_messages(chat_id,user_id)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            for msg in messages:
                if msg.sender_id.id != user_id and user_id not in msg.seen_by:
                    msg.seen_by.append(user_id)
                    msg.save()
                    
            messages_data = [
                {
                    'id': msg.id,
                    'text': msg.text,
                    'audio_msg':msg.audio_url,
                    'created_at': msg.created_at.strftime("%I:%M %p"),
                    'sender_id': msg.sender_id.id,
                    'sender_name': f"{msg.sender_id.first_name} {msg.sender_id.last_name}",
                    'is_edited': msg.is_edited,
                    'reactions': reactions_service.get_message_reaction(msg.id),
                    'seen_by': msg.seen_by,
                    'member_count': msg.chat.members.count(),
                    'reply_to': {
                        'id': msg.reply_for_message.id,
                        'text': msg.reply_for_message.text,
                    } if msg.reply_for_message else None,

                }
                for msg in messages
            ]
            return JsonResponse({
                'status': 'success',
                'chat_id': chat_id,
                'messages': messages_data, 
                'emojies' : reactions_service.get_all_emojies()
            })
class MessageCreateView(View):   
    def post(self, request, chat_id):
        try:
            message_text = request.POST.get('message_text')
            reply_to = request.POST.get('reply_to')
            if not message_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'message_text is required'
                }, status=400)
                
            message = message_service.create_message(
                text=message_text,
                chat_id=chat_id,
                sender_id=request.user.id,
                created_by_id=request.user.id,
                reply_for_message_id=reply_to
            )
            
            if message:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Message sent successfully',
                    'data': {
                        'id': message.id,
                        'text': message.text,
                        'created_at': message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        'sender_id': message.sender_id.id,
                        'sender_name': f"{message.sender_id.first_name} {message.sender_id.last_name}"
                    }
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to create message'
            }, status=500)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

        


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class MessageUpdateView(View):
    def post(self, request, message_id):
        try:
            message_text = request.POST.get('message_text')
            chat_id = request.POST.get('chat_id')
            
            if not message_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'message_text is required'
                }, status=400)
                
            message = message_service.update_message(
                message_id=message_id,
                text=message_text,
                updated_by_id=request.user.id
            )
            
            if message:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Message updated successfully',
                    'data': {
                        'id': message.id,
                        'text': message.text,
                        'updated_at': message.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        'is_edited': message.is_edited
                    }
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Message not found or you are not the sender'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
            
            
            
@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class MessageDeleteView(View):
    def post(self, request, message_id):
        try:
            data = json.loads(request.body)
            purpose = data.get('purpose')
            message = message_service.get_message_object(message_id, request.user.id)
            
            deleted = message_service.delete_message(message_id,purpose,request.user)
            
            if deleted:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Message deleted successfully'
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to delete message'
            }, status=500)
            
        except message.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Message not found or you are not the sender'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
        

class SendAudioMessageView(View):
    def post(self,request):
        audio_file = request.FILES.get("audio")
        chat_id = request.POST.get("chat_id")
        sender = request.user

        if not audio_file or not chat_id:
            return JsonResponse({"success": False, "error": "Missing audio or chat_id"})

        message = message_service.voice_message_create(audio_file,chat_id ,sender)
        return JsonResponse({"success": True, "audio_url": message.audio_url, "message_id": message.id})


@auth_required
@role_required(Role.END_USER.value, page_type='enduser')
class MessageReactView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            message_id = data.get('message_id')
            emoji_id = data.get('emoji_id')
            user_id = request.user.id

            if not message_id or not emoji_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Message ID and Emoji ID are required'
                }, status=400)

            # Check if user already has a reaction on this message
            existing_reaction = MessageReaction.objects.filter(
                message=message_id,
                reacted_by=user_id,
                is_active=True
            ).first()

            if existing_reaction:
                if existing_reaction.reaction_id == emoji_id:
                    # Same emoji clicked - remove reaction
                    existing_reaction.is_active = False
                    existing_reaction.save()
                else:
                    # Different emoji clicked - update existing reaction
                    existing_reaction.reaction_id = emoji_id
                    existing_reaction.save()
            else:
                # Add new reaction
                MessageReaction.objects.create(
                    message_id=message_id,
                    reacted_by_id=user_id,
                    reaction_id=emoji_id,
                    created_by_id=user_id,
                    updated_by_id=user_id
                )

            # Get all active reactions for this message to return
            reactions = MessageReaction.objects.filter(
                message=message_id,
                is_active=True
            ).select_related('reaction')

            reactions_data = []
            for reaction in reactions:
                reactions_data.append({
                    'id': reaction.id,
                    'value': reaction.reaction.value,
                    'is_current_user': reaction.reacted_by_id == user_id
                })

            return JsonResponse({
                'status': 'success',
                'reactions': reactions_data
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)