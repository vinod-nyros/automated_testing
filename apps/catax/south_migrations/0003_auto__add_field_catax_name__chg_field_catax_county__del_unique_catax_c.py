# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Removing unique constraint on 'Catax', fields ['county', 'tax']
        #db.delete_unique(u'catax', ['county', 'tax'])

        # Removing unique constraint on 'Catax', fields ['county']
        #db.delete_unique(u'catax', ['county'])

        # Adding field 'Catax.name'
        db.add_column(u'catax', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Changing field 'Catax.county'
        db.alter_column(u'catax', 'county', self.gf('django.db.models.fields.CharField')(max_length=50))


    def backwards(self, orm):

        # Deleting field 'Catax.name'
        db.delete_column(u'catax', 'name')

        # Changing field 'Catax.county'
        db.alter_column(u'catax', 'county', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True))

        # Adding unique constraint on 'Catax', fields ['county']
        db.create_unique(u'catax', ['county'])

        # Adding unique constraint on 'Catax', fields ['county', 'tax']
        db.create_unique(u'catax', ['county', 'tax'])


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
            'cities': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1000', 'blank': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['catax']
