# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Cacountycounts'
        db.delete_table(u'cacountycounts')

        # Deleting model 'Cacountytax'
        db.delete_table(u'cacountytax')

        # Deleting model 'Cacountytaxcounts'
        db.delete_table(u'cacountytaxcounts')

        # Deleting model 'Cacounties'
        db.delete_table(u'cacounties')

        # Deleting model 'Catax'
        db.delete_table(u'catax')


    def backwards(self, orm):
        
        # Adding model 'Cacountycounts'
        db.create_table(u'cacountycounts', (
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('catax', ['Cacountycounts'])

        # Adding model 'Cacountytax'
        db.create_table(u'cacountytax', (
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('catax', ['Cacountytax'])

        # Adding model 'Cacountytaxcounts'
        db.create_table(u'cacountytaxcounts', (
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('catax', ['Cacountytaxcounts'])

        # Adding model 'Cacounties'
        db.create_table(u'cacounties', (
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('catax', ['Cacounties'])

        # Adding model 'Catax'
        db.create_table(u'catax', (
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('cities', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1000, blank=True)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('catax', ['Catax'])


    models = {
        
    }

    complete_apps = ['catax']
