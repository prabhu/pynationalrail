from django.contrib.auth.models import User

def create_user(request, username, password):
    """
    Method to create a user.
    """
    user = User.objects.create_user(username, '', password)
    user.is_staff = True
    user.save()
    return user
