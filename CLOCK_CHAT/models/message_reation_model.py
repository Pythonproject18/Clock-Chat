from django.db import models


class MessageReaction(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='message_reaction_message_id')
    reacted_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reacted_by_reaction_users_id')
    reaction = models.ForeignKey('Reaction', on_delete=models.CASCADE, related_name='reation_message_reaction_reation_id')


    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='created_chat_members')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reactions_updated')


    class Meta:
                db_table = 'message_reactions'

def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"