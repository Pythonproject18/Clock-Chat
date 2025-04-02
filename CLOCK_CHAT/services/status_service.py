from CLOCK_CHAT.models import Friend,Status
from django.db.models import Q
from django.core.exceptions import ValidationError



def get_friends_by_user(user_id):

    # Fetch friends where user is either the initiator or recipient
    friends = Friend.objects.filter(
        Q(user_id=user_id) | Q(friend_id=user_id), is_active=True
    ).distinct()

    friend_data = []
    friend_ids = set()  # Track unique friend IDs

    for friend in friends:
        # Get the actual friend object, excluding the user themselves
        friend_obj = friend.friend if friend.user_id == user_id else friend.user

        if friend_obj.id != user_id and friend_obj.id not in friend_ids:
            friend_ids.add(friend_obj.id)  # Add ID to set to prevent duplicates
            
            latest_status = Status.objects.filter(
                created_by=friend_obj, is_active=True
            ).order_by('-created_at').first()

            friend_data.append({
                'id': friend_obj.id,
                'name': f"{friend_obj.first_name} {friend_obj.last_name}",  # Space added between names
                'email': friend_obj.email,  # Assuming Friend model has an `email` field
                'status_media': latest_status.status_media if latest_status else None,
                'created_at': latest_status.created_at if latest_status else None,
            })

    return friend_data

def get_user_status(user_id):
    
        latest_status = Status.objects.filter(
            created_by=user_id, is_active=True
        ).order_by('-created_at').first()
        
        if latest_status:
            return {
                'id': latest_status.id,
                'status_media': latest_status.status_media if latest_status.status_media else None,
                'created_by': latest_status.created_by if latest_status else None,
            }
   

def create_status(image, user_id, status_type):
    try:
        status = Status.objects.create(
            media=image,  # Fixed field name
            status_type=status_type,
            created_by_id=user_id  # Ensure it matches the User model's ID
        )
        return {'success': True, 'message': 'Status created successfully', 'status_id': status.id}
    
    except ValidationError as e:
        return {'success': False, 'message': str(e)}
    
    except Exception as e:
        return {'success': False, 'message': 'Something went wrong: ' + str(e)}


        

    