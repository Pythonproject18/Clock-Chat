from django.db import models
from ..constants import Status_Type

class Status(models.Models):
       
       status_media = models.URLField(max_length=255, blank=True, null=True)
       status_type = models.IntegerField(
        choices=[(stype.value, stype.name) for stype in Status_Type],
        null=True,blank=True
       )
       viewers = models.ManyToManyField(
          'User',
          through='StatusViewer',
          through_fields=('status','viewed_by'),
          related_name= 'fk_viewers_Status_users_id'
       )

       is_active = models.BooleanField(default=True)
       created_at =models.DateTimeField(auto_now_add=True)
       updated_at =models.DateTimeField(auto_now=True, null=True, blank=True)
       created_by= models.ForeignKey( 'User', on_delete=models.CASCADE, related_name='fk_user_status_create_users_id', blank=True)
       updated_by=models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_status_update_users_id', null=True, blank=True)

       class Meta:
        db_table = 'status'


       def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"