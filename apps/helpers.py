from django.db import connection
from django.conf import settings

trace = 0


def get_next_id():
    cursor = connection.cursor()
    cursor.execute("select nextval('ids')")
    row = cursor.fetchone()
    return row [0]


#from django.db.models.signals import pre_save

if settings.TESTING:
  def presave (sender=None, instance=None, **kw): 
    pass
else:
  def presave (sender=None, instance=None, **kw):
    if trace: print 'PRESAVE:', sender, instance, instance.id

    if instance and not instance.id:
        instance.id = get_next_id()

    if trace: print 'PRESAVE RESULT:', instance.id

#pre_save.connect (presave, sender=ProductOption)
