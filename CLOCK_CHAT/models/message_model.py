from django.db import models
from ..constants import Delete_Type
from django.contrib.postgres.fields import ArrayField


class Message(models.Model):
    text = models.CharField(max_length=300, blank=True, null=True)
    message_media = models.URLField(max_length=255,blank=True, null=True)
    audio_url = models.URLField(max_length=255,blank=True, null=True)
    mentions = ArrayField(
        models.IntegerField(),
        blank=True,
        default=list
        )
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='fk_chat_messege_chats_id')
    reply_for_message = models.ForeignKey('Message', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_reply_message_messages_id')
    sender_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_messages_created')
    seen_by = ArrayField(
        models.IntegerField(),
        blank=True,
        default=list
        )
    del_type = models.IntegerField(
        choices=[(ctype.value, ctype.name) for ctype in Delete_Type],
        null=True,blank=True
        )
    del_by = ArrayField(
        models.IntegerField(),
        blank=True,
        default=list
        )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_message_created_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_message_updated_users_id')

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"