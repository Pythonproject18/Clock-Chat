from django.db import models

class Reaction(models.Model):
   name=models.CharField(max_length=50)
   value= models.CharField(max_length=50)
   

   is_active= models.BooleanField(default=True)
   created_at= models.DateTimeField(auto_now_add=True)
   updated_at= models.DateTimeField(auto_now=True ,blank=True, null=True)
   created_by=models.ForeignKey('User',on_delete=models.CASCADE, related_name='fk_user_reactions_created_users_id')
   updated_by=models.ForeignKey('User', on_delete=models.SET_NULL, related_name='fk_user_reactions_updated_users_id', null=True, blank=True)



class Meta:
        db_table = 'reactions'

    
def __str__(self):
        return f"ID: {self.id}, Created_at: {self.created_at}, Active: {self.is_active}"
 