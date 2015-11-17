#from django.db import models
#from django.db.models.signals import class_prepared
#from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

print 'Monkey patching!'
User._meta.get_field("username").max_length = 128
User._meta.get_field("email").max_length = 128
