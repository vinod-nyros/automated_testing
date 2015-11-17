# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Cacounties'
        db.create_table(u'cacounties', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('catax', ['Cacounties'])

        # Adding model 'Cacountytax'
        db.create_table(u'cacountytax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('catax', ['Cacountytax'])

        # Adding model 'Cacountycounts'
        db.create_table(u'cacountycounts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('catax', ['Cacountycounts'])

        # Adding model 'Cacountytaxcounts'
        db.create_table(u'cacountytaxcounts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('catax', ['Cacountytaxcounts'])

        # Adding model 'Catax'
        db.create_table(u'catax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('catax', ['Catax'])


    def backwards(self, orm):
        
        # Deleting model 'Cacounties'
        db.delete_table(u'cacounties')

        # Deleting model 'Cacountytax'
        db.delete_table(u'cacountytax')

        # Deleting model 'Cacountycounts'
        db.delete_table(u'cacountycounts')

        # Deleting model 'Cacountytaxcounts'
        db.delete_table(u'cacountytaxcounts')

        # Deleting model 'Catax'
        db.delete_table(u'catax')


    models = {
        'catax.cacounties': {
            'Meta': {'object_name': 'Cacounties', 'db_table': "u'cacounties'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'catax.cacountycounts': {
            'Meta': {'object_name': 'Cacountycounts', 'db_table': "u'cacountycounts'"},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'catax.cacountytax': {
            'Meta': {'object_name': 'Cacountytax', 'db_table': "u'cacountytax'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'catax.cacountytaxcounts': {
            'Meta': {'object_name': 'Cacountytaxcounts', 'db_table': "u'cacountytaxcounts'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'catax.catax': {
            'Meta': {'object_name': 'Catax', 'db_table': "u'catax'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['catax']
