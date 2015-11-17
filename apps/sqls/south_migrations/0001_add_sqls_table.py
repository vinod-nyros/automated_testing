# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
#from django_eracks.apps.sqls.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'Sql'
        db.create_table('sqls_sql', (
            ('id', orm['sqls.sql:id']),
            ('description', orm['sqls.sql:description']),
            ('sql', orm['sqls.sql:sql']),
            ('created', orm['sqls.sql:created']),
            ('modified', orm['sqls.sql:modified']),
        ))
        db.send_create_signal('sqls', ['Sql'])



    def backwards(self, orm):

        # Deleting model 'Sql'
        # JJW - comment out, this is too dangerous -
        pass
        #db.delete_table('sqls_sql')



    models = {
        'sqls.sql': {
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'sql': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['sqls']
