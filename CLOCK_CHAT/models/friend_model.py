from django.db import models

class Friend(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE, related_name='fk_user_friend_users_id')
    friend = models.ForeignKey('User',on_delete=models.CASCADE, related_name='fk_friend_friend_users_id')

    is_active= models.BooleanField (default=True, blank=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by= models.ForeignKey( 'User', on_delete=models.CASCADE, related_name='fk_user_friend_create_users_id', blank=True)
    updated_by=models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_friend_update_users_id', null=True, blank=True)

    class Meta:
        db_table = 'friends'


    def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"