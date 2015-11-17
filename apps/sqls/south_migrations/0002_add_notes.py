# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
#from django_eracks.apps.sqls.models import *

class Migration:

    def forwards(self, orm):

        # Adding field 'Sql.notes'
        db.add_column('sqls_sql', 'notes', orm['sqls.sql:notes'])



    def backwards(self, orm):

        # Deleting field 'Sql.notes'
        db.delete_column('sqls_sql', 'notes')



    models = {
        'sqls.sql': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'sql': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['sqls']
