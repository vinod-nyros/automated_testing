# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from eracks9.apps.sqls.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Sql'
        db.create_table('sqls_sql', (
            ('id', orm['sqls.sql:id']),
            ('description', orm['sqls.sql:description']),
            ('sql', orm['sqls.sql:sql']),
            ('parm1', orm['sqls.sql:parm1']),
            ('parm2', orm['sqls.sql:parm2']),
            ('parm3', orm['sqls.sql:parm3']),
            ('parm4', orm['sqls.sql:parm4']),
            ('parm5', orm['sqls.sql:parm5']),
            ('notes', orm['sqls.sql:notes']),
            ('created', orm['sqls.sql:created']),
            ('modified', orm['sqls.sql:modified']),
        ))
        db.send_create_signal('sqls', ['Sql'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Sql'
        db.delete_table('sqls_sql')
        
    
    
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
