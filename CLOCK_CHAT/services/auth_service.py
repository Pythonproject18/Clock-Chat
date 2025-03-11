from ..models import User

def create_user(first_name,middle_name,last_name,email):
    User.objects.create(
        first_name=first_name,
        middle_name= middle_name,
        last_name= last_name,
        email=email
    )
    return