# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
#from django_eracks.apps.sqls.models import *

class Migration:

    def forwards(self, orm):

        # Adding field 'Sql.updates'
        db.add_column('sqls_sql', 'updates', orm['sqls.sql:updates'])



    def backwards(self, orm):

        # Deleting field 'Sql.updates'
        db.delete_column('sqls_sql', 'updates')



    models = {
        'sqls.sql': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '30', 'blank': 'True'}),
            'parm1': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'parm2': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'parm3': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'parm4': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'parm5': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'sql': ('django.db.models.fields.TextField', [], {}),
            'updates': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['sqls']
