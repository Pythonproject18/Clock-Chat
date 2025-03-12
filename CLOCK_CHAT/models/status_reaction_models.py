from django.db import models

class StatusReaction(models.Model):
    
    status= models.ForeignKey('Status', on_delete=models.CASCADE, related_name='fk_status_status_reactions_status_id')
    reacted_by= models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_status_reactions_users_id')
    reaction=models.ForeignKey('Reaction', on_delete=models.CASCADE, related_name='fk_reaction_status_reaction_reactions_id')

    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True,blank=True, null=True)
    created_by=models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_status_reactions_created_users_id')
    updated_by=models.ForeignKey('User', on_delete=models.CASCADE, related_name="fk_user_status_reactions_updated_users_id", null=True, blank=True)


    
    class Meta:
        db_table = 'status_reactions'

    
    def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"
