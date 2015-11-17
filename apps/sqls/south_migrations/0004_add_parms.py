# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
#from django_eracks.apps.sqls.models import *

class Migration:

    def forwards(self, orm):

        # Adding field 'Sql.parm5'
        db.add_column('sqls_sql', 'parm5', orm['sqls.sql:parm5'])

        # Adding field 'Sql.parm2'
        db.add_column('sqls_sql', 'parm2', orm['sqls.sql:parm2'])

        # Adding field 'Sql.parm4'
        db.add_column('sqls_sql', 'parm4', orm['sqls.sql:parm4'])

        # Adding field 'Sql.parm1'
        db.add_column('sqls_sql', 'parm1', orm['sqls.sql:parm1'])

        # Adding field 'Sql.parm3'
        db.add_column('sqls_sql', 'parm3', orm['sqls.sql:parm3'])



    def backwards(self, orm):

        # Deleting field 'Sql.parm5'
        db.delete_column('sqls_sql', 'parm5')

        # Deleting field 'Sql.parm2'
        db.delete_column('sqls_sql', 'parm2')

        # Deleting field 'Sql.parm4'
        db.delete_column('sqls_sql', 'parm4')

        # Deleting field 'Sql.parm1'
        db.delete_column('sqls_sql', 'parm1')

        # Deleting field 'Sql.parm3'
        db.delete_column('sqls_sql', 'parm3')



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
            'sql': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['sqls']
