from django.db import models
from django.db.models import Q
from ..constants import Chat_Type


class Chat(models.Model):
    chat_title = models.CharField(max_length=50, null=True, blank=True)
    chat_cover_photo = models.URLField(max_length=255, null=True, blank=True)
    chat_bio = models.CharField(max_length=50, null=True, blank=True)
    type = models.IntegerField(
        choices=[(ctype.value, ctype.name) for ctype in Chat_Type],
        null=True,blank=True
        )
    members = models.ManyToManyField('User', through='ChatMember' , through_fields=('chat','member') ,related_name='fk_members_chats_users')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_chats_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_chats_users_id')
    is_active = models.BooleanField(default=True)
    

    class Meta:
        db_table = 'chats'
        constraints = [
            models.CheckConstraint(
                check=~Q(type=Chat_Type.Personal.value) | (Q(chat_title__isnull=True) & Q(chat_bio__isnull=True)),
                name="personal_chat_no_title_bio"
            )
        ]

    def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"