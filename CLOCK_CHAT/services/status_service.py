from CLOCK_CHAT.models import Friend,Status,User
from django.db.models import Q
from django.core.exceptions import ValidationError
from CLOCK_CHAT.constants.default_values import Status_Type



def get_friends_by_user(user_id):
    # Fetch all friend relationships involving the user
    friends = Friend.objects.filter(
        Q(user_id=user_id) | Q(friend_id=user_id),
        is_active=True
    ).distinct()

    friend_ids = set()

    for friend in friends:
        # Get the other user's ID (not the current user)
        other_id = friend.friend_id if friend.user_id == user_id else friend.user_id
        friend_ids.add(other_id)

    # Filter only friends with at least one active status
    friends_with_active_status = User.objects.filter(
        id__in=friend_ids,
        fk_user_status_create_users_id__is_active=True
    ).distinct()

    friend_data = []
    for friend_obj in friends_with_active_status:
        # Get the latest active status of the friend
        latest_status = Status.objects.filter(
            created_by=friend_obj, is_active=True
        ).order_by('-created_at').first()

        friend_data.append({
            'id': friend_obj.id,
            'name': f"{friend_obj.first_name} {friend_obj.last_name}".strip(),
            'email': friend_obj.email,
            'status_media': latest_status.status_media if latest_status else None,
            'created_at': latest_status.created_at if latest_status else None,
            'caption':latest_status.caption
        })

    return friend_data


def get_user_status(user_id):
    
        latest_status = Status.objects.filter(
            created_by=user_id, is_active=True
        ).order_by('-created_at').first()
        
        if latest_status:
            return {
                'user_id':user_id,
                'id': latest_status.id,
                'status_media': latest_status.status_media if latest_status.status_media else None,
                'created_by': latest_status.created_by if latest_status else None,
            }
   

def create_status(image, user_id, status_type,caption):
    user=User.objects.filter(id=user_id,is_active=True).first()
    type= Status_Type(int(status_type)).value
    status = Status.objects.create(
        status_media=image,  # Fixed field name
        status_type=type,
        created_by=user,  # Ensure it matches the User model's ID
        caption = caption
    )
    return status

def get_all_status_by_user_id(user_id):
    return Status.objects.filter(created_by=user_id).order_by('-created_at')




        

    