# Originally from https://github.com/aRkadeFR/django-generate-fixtures - see also my fork under jowolf :)

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from django.db import models
from django.db.models import Model
from django.core import serializers
import importlib
import sys

trace = 0

seen = []

def _get_data(obj):
    """
    fetch all the data of the object.
    follow the sets etc.
    """
    if not isinstance(obj, models.Model):
        raise Exception('Not a model')

    ans = []
    uid = repr(obj)
    if uid in seen:
        return ans
    seen.append(uid)

    # adding the reverse set
    for d in [d for d in dir(obj) if not d.startswith('_')]:
        if trace: print obj, d,
        try:
            attr = getattr(obj, d)
            if trace: print attr.__class__, isinstance (attr, models.Manager)
        except Exception, e:
            if trace: print 'Exception:', e
            pass

        #if d in [ field.name for field in obj.__class__._meta.fields ]:
        if d in [ f.name for f in obj.__class__._meta.many_to_many ]:
          #mgr = obj.__class__._meta.get_field (d)
          #print mgr
          if isinstance (attr, models.Manager):  # it's an m2m field
            if trace: print 'M2M' #, attr
            set_objs = attr.all()
            for set_obj in set_objs:
                ans += _get_data(set_obj)  # so recurse
          #elif isinstance (attr, models.ForeignKey):  # it's me pointing out to another object
          #  if trace: print 'FK:', attr
          #  ans += _get_data(attr)  # so recurse

        # Foreign keys come through directly as Managers

        if isinstance(attr, models.Model):
            ans += _get_data(attr)

    ans.append(obj)

    return ans


def generate_data(obj):
    ans = []
    if not isinstance(obj, Model):
        raise Exception('No model to follow')
    else:
        ans += _get_data(obj)

    return ans


class Command(BaseCommand):
    args = '<app>.<Model> <id_object> [<max_depth>]'
    help = """
           Generate fixtures
           for a given object, generate yaml fixtures to redirect
           to a file in order to have full hierarchy of models
           from this parent object.

           syntax example:
               python manage.py generate_fixtures 'core.models.Client' 364 > ./core/fixtures/test_fixtures.yaml
           """

    def handle(self, *args, **options):
        if len(args) == 2:
            app_model = args[0]
            pk = args[1]  # TODO:  split into list on commas present, and loop
            module_name = '.'.join(app_model.split('.')[0:-1])
            model_name = app_model.split('.')[-1]
            module = importlib.import_module(module_name)
            if module:
                model = getattr(module, model_name)
                try:
                    parent_obj = model.objects.get(pk=pk)
                    self.stderr.write("fetched the parent obj {}\n".format(parent_obj))
                except:
                    raise CommandError("didnt find the object with the pk {}".format(pk))

                data = generate_data(parent_obj)

                self.stdout.write(
                    serializers.serialize("yaml", data, indent=4)
                )
                self.stderr.write("done\n\n")
            else:
                raise CommandError("No module named {}".format(module_name))
        else:
            raise CommandError(self.help)
