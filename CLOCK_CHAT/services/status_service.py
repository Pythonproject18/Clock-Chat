from CLOCK_CHAT.models import Friend
def get_friends_by_user(user_id):
    friends = Friend.objects.filter(user=user_id, is_active = True ).values('friend') and Friend.objects.filter(friend= user_id , is_active =True).values('user')
    print(friends)
    return