from django.db import models
from django.contrib.auth.models import User, Group

from common.middleware import get_current_user

class Favorite(models.Model):
    """
    Model representing a favorite
    """
    user = models.ForeignKey(User, help_text="Owner user")
    fname = models.CharField(max_length=100, help_text="Favorite name")
    ftype = models.CharField(max_length=30, help_text="Favorite type")
    fromS = models.CharField(max_length=30, help_text="From station")
    viaS = models.CharField(max_length=30, help_text="Via station")
    
    def __unicode__(self):
        return u'%s' %(self.fname)
    
    def save(self, **args):
        if not self.user:
            user = get_current_user()
            if user:
                self.user = user
        super(Favorite, self).save(args)
