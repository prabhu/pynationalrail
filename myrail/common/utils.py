from django.contrib.auth.models import User
import traceback

def create_user(request, username, password):
    """
    Method to create a user.
    """
    user = User.objects.create_user(username, '', password)
    user.is_staff = True
    user.save()
    return user

# Decorators
def debugger(action):
    """
    Decorator to check for mandatory parameters
    """
    def func(*args, **kwargs):
        try:
            return action(*args, **kwargs)
        except:
            traceback.print_exc()
    return func
