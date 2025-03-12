from django.db import models
from django.contrib.postgres.fields import ArrayField


class ChatMember(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='fk_chat_cmember_chats_id')
    member = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_member_cmember_users_id')
    is_admin = ArrayField(
        models.IntegerField(),
        blank=True,
        default=list
        )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='fk_created_chat_member_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='fk_updated_chat_member_users_id')
    

class Meta:
        db_table = 'chat_members'

def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"