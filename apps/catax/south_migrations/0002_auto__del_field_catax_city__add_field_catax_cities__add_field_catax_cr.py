# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Deleting field 'Catax.city'
        db.delete_column(u'catax', 'city')

        # Adding field 'Catax.cities'
        db.add_column(u'catax', 'cities', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=1000, blank=True), keep_default=False)

        # Adding field 'Catax.created'
        db.add_column(u'catax', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date(2012, 4, 11), blank=True), keep_default=False)

        # Adding field 'Catax.updated'
        db.add_column(u'catax', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(2012, 4, 11), blank=True), keep_default=False)

        # Changing field 'Catax.county'
        db.alter_column(u'catax', 'county', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100))

        # Adding unique constraint on 'Catax', fields ['county']
        #db.create_unique(u'catax', ['county'])

        # Changing field 'Catax.tax'
        db.alter_column(u'catax', 'tax', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2))

        # Adding unique constraint on 'Catax', fields ['county', 'tax']
        #db.create_unique(u'catax', ['county', 'tax'])


    def backwards(self, orm):

        # Removing unique constraint on 'Catax', fields ['county', 'tax']
        db.delete_unique(u'catax', ['county', 'tax'])

        # Removing unique constraint on 'Catax', fields ['county']
        db.delete_unique(u'catax', ['county'])

        # User chose to not deal with backwards NULL issues for 'Catax.city'
        raise RuntimeError("Cannot reverse this migration. 'Catax.city' and its values cannot be restored.")

        # Deleting field 'Catax.cities'
        db.delete_column(u'catax', 'cities')

        # Deleting field 'Catax.created'
        db.delete_column(u'catax', 'created')

        # Deleting field 'Catax.updated'
        db.delete_column(u'catax', 'updated')

        # Changing field 'Catax.county'
        db.alter_column(u'catax', 'county', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Catax.tax'
        db.alter_column(u'catax', 'tax', self.gf('django.db.models.fields.FloatField')())


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
            'Meta': {'unique_together': "(('county', 'tax'),)", 'object_name': 'Catax', 'db_table': "u'catax'"},
            'cities': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1000', 'blank': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['catax']
