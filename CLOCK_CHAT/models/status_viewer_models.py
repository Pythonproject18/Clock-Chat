from django.db import models

class StatusViewer(models.Model):
    status = models.ForeignKey( 'Status',on_delete=models.CASCADE, related_name='fk_status_status_viewer_status_id')
    viewed_by = models.ForeignKey('User',on_delete=models.CASCADE, related_name='fk_user_status_viewer_users_id')


    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_status_viewers_created_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_status_viewers_updated_users_id', null=True, blank=True)

    class Meta:
        db_table = 'status_viewers'

    
    def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"