from CLOCK_CHAT.models import Friend,Status,User,StatusViewer
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.core.files.storage import default_storage
from django.conf import settings
import os

def get_friends_by_user(user_id):
    is_active_status()
    
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

        if latest_status:  # Only add if there is a status
            friend_data.append({
                'id': friend_obj.id,
                'name': f"{friend_obj.first_name} {friend_obj.last_name}".strip(),
                'email': friend_obj.email,
                'status_media': latest_status.status_media,
                'created_at': latest_status.created_at,
                'is_seen': check_status_seen_or_not(friend_obj.id, user_id),
            })

    # Sort the friend_data by latest status time, descending
    friend_data.sort(key=lambda x: x['created_at'], reverse=True)

    return friend_data


def is_active_status():
    now = timezone.now()

    # Get all statuses that are active and older than 12 hours
    old_statuses = Status.objects.filter(
        is_active=True,
        created_at__lte=now - timedelta(hours=12)  # Filter for statuses older than 12 hours
    )

    # Deactivate all statuses older than 12 hours
    for oldstatus in old_statuses:
        oldstatus.is_active = False
        oldstatus.save()

    return old_statuses  

def get_user_status(user_id):
    is_active_status()
    latest_status = Status.objects.filter(
        created_by=user_id, is_active=True
    ).order_by('created_at').first()
    
    if latest_status:
        return {
            'user_id':user_id,
            'id': latest_status.id,
            'status_media': latest_status.status_media if latest_status.status_media else None,
            'created_by': latest_status.created_by if latest_status else None,
        }
   

def create_status(image, user_id, status_type,caption):
    user=User.objects.filter(id=user_id,is_active=True).first()
    status = Status.objects.create(
        status_media=image,  # Fixed field name
        status_type = status_type,
        created_by=user,  # Ensure it matches the User model's ID
        caption = caption
    )
    return status

def get_all_status_by_user_id(user_id):
    is_active_status()
    return Status.objects.filter(created_by=user_id,is_active = True).order_by('created_at')


def get_status_viewer(status_id):
    return list(StatusViewer.objects.filter(status_id=status_id,is_active=True).values('viewed_by'))


def status_viewer_create(status, current_user, created_by):
    if not StatusViewer.objects.filter(status=status.id, viewed_by=current_user).exists():
        StatusViewer.objects.create(
            status=status,
            viewed_by=current_user,
            created_by=created_by
        )

def get_status_viewers_count(status_id,user):
    return StatusViewer.objects.filter(status = status_id,is_active=True).exclude(viewed_by = user).count()

def check_status_seen_or_not(user_id, current_user):
    # Get all active statuses created by the friend
    statuses = Status.objects.filter(created_by=user_id, is_active=True)

    # Get all status IDs
    status_ids = statuses.values_list('id', flat=True)

    # Get all status IDs that the current user has viewed
    seen_status_ids = StatusViewer.objects.filter(
        status_id__in=status_ids,
        viewed_by=current_user,
        is_active=True
    ).values_list('status_id', flat=True)

    # Return True only if all statuses have been seen, else False
    if set(status_ids) == set(seen_status_ids):
        return True
    else:
        return False
    

def delete_temp_status_file():
    """
    Deletes all files in the 'media/status_preview/' directory.
    """
    preview_dir = os.path.join(settings.MEDIA_ROOT, 'status_preview')

    if os.path.exists(preview_dir):
        for filename in os.listdir(preview_dir):
            file_path = os.path.join(preview_dir, filename)
            if os.path.isfile(file_path):
                default_storage.delete(os.path.relpath(file_path, settings.MEDIA_ROOT))
        return True
    return False

        
        

    