from django.db import models
from django.contrib.postgres.fields import ArrayField


class ChatMember(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='members')
    member = models.ForeignKey('User', on_delete=models.CASCADE, related_name='chat_memberships')
    is_admin = ArrayField(
        models.IntegerField(),
        blank=True,
        default=list
        )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='created_chat_members')
    updated_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='updated_chat_members')
    

class Meta:
        db_table = 'chatmembers'

def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"