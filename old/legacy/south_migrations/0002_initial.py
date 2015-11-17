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
        db.send_create_signal('legacy', ['Cacounties'])

        # Adding model 'Cacountytax'
        db.create_table(u'cacountytax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('legacy', ['Cacountytax'])

        # Adding model 'Cacountycounts'
        db.create_table(u'cacountycounts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('legacy', ['Cacountycounts'])

        # Adding model 'Cacountytaxcounts'
        db.create_table(u'cacountytaxcounts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('legacy', ['Cacountytaxcounts'])

        # Adding model 'Catax'
        db.create_table(u'catax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('legacy', ['Catax'])

        # Adding model 'PgaQueries'
        db.create_table(u'pga_queries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('queryname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('querytype', self.gf('django.db.models.fields.TextField')()),
            ('querycommand', self.gf('django.db.models.fields.TextField')()),
            ('querytables', self.gf('django.db.models.fields.TextField')()),
            ('querylinks', self.gf('django.db.models.fields.TextField')()),
            ('queryresults', self.gf('django.db.models.fields.TextField')()),
            ('querycomments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['PgaQueries'])

        # Adding model 'PgaForms'
        db.create_table(u'pga_forms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('formname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('formsource', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['PgaForms'])

        # Adding model 'PgaScripts'
        db.create_table(u'pga_scripts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scriptname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('scriptsource', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['PgaScripts'])

        # Adding model 'PgaReports'
        db.create_table(u'pga_reports', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reportname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('reportsource', self.gf('django.db.models.fields.TextField')()),
            ('reportbody', self.gf('django.db.models.fields.TextField')()),
            ('reportprocs', self.gf('django.db.models.fields.TextField')()),
            ('reportoptions', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['PgaReports'])

        # Adding model 'PgaLayout'
        db.create_table(u'pga_layout', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tablename', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('nrcols', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('colnames', self.gf('django.db.models.fields.TextField')()),
            ('colwidth', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['PgaLayout'])

        # Adding model 'PgaGraphs'
        db.create_table(u'pga_graphs', (
            ('graphname', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('graphsource', self.gf('django.db.models.fields.TextField')()),
            ('graphcode', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['PgaGraphs'])

        # Adding model 'PgaImages'
        db.create_table(u'pga_images', (
            ('imagename', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('imagesource', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['PgaImages'])

        # Adding model 'PgaDiagrams'
        db.create_table(u'pga_diagrams', (
            ('diagramname', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('diagramtables', self.gf('django.db.models.fields.TextField')()),
            ('diagramlinks', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['PgaDiagrams'])

        # Adding model 'Costspersku'
        db.create_table(u'costspersku', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('defaultcost', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('legacy', ['Costspersku'])

        # Adding model 'Optchoices'
        db.create_table(u'optchoices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('optid', self.gf('django.db.models.fields.IntegerField')()),
            ('choiceid', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('legacy', ['Optchoices'])

        # Adding model 'Optionchoices'
        db.create_table(u'optionchoices', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('optionid', self.gf('django.db.models.fields.IntegerField')()),
            ('choiceid', self.gf('django.db.models.fields.IntegerField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('legacy', ['Optionchoices'])

        # Adding model 'ChoiceCategory'
        db.create_table(u'choicecategories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sohigh', self.gf('django.db.models.fields.IntegerField')()),
            ('solow', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('legacy', ['ChoiceCategory'])

        # Adding model 'Choice'
        db.create_table(u'choices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('current', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('supplier', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('cost', self.gf('django.db.models.fields.FloatField')()),
            ('avehours', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('sortorder', self.gf('django.db.models.fields.IntegerField')()),
            ('multiplier', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('choicecategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legacy.ChoiceCategory'])),
        ))
        db.send_create_signal('legacy', ['Choice'])

        # Adding model 'Option'
        db.create_table(u'options', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('dependencies', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('avehours', self.gf('django.db.models.fields.IntegerField')()),
            ('faq', self.gf('django.db.models.fields.TextField')()),
            ('sortorder', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('legacy', ['Option'])

        # Adding model 'Product'
        db.create_table(u'products', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sku', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('baseprice', self.gf('django.db.models.fields.FloatField')()),
            ('cost', self.gf('django.db.models.fields.FloatField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legacy.Categories'], db_column='categoryid')),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
            ('pix', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('baseoptions', self.gf('django.db.models.fields.CharField')(max_length=254, blank=True)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('current', self.gf('django.db.models.fields.CharField')(default='T', max_length=1)),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('algorithm', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sortorder', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('multiplier', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
        ))
        db.send_create_signal('legacy', ['Product'])

        # Adding model 'Categories'
        db.create_table(u'categories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['Categories'])

        # Adding model 'Prodopt'
        db.create_table(u'prodopts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legacy.Product'], db_column='productid')),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legacy.Option'], db_column='optionid')),
            ('defaultchoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legacy.Choice'], db_column='defaultchoiceid')),
        ))
        db.send_create_signal('legacy', ['Prodopt'])

        # Adding model 'Prodoptchoice'
        db.create_table(u'prodoptchoices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('pricedelta', self.gf('django.db.models.fields.FloatField')()),
            ('productoption', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legacy.Prodopt'], db_column='productoptionid')),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legacy.Choice'], db_column='choiceid')),
            ('current', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('legacy', ['Prodoptchoice'])

        # Adding model 'Addresses'
        db.create_table(u'addresses', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('customerid', self.gf('django.db.models.fields.IntegerField')()),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('legacy', ['Addresses'])

        # Adding model 'Orders'
        db.create_table(u'orders', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('customerid', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('shipping', self.gf('django.db.models.fields.FloatField')()),
            ('shippingmethod', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dtprocessed', self.gf('django.db.models.fields.DateTimeField')()),
            ('returned', self.gf('django.db.models.fields.TextField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('legacy', ['Orders'])

        # Adding model 'Emails'
        db.create_table(u'emails', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customerid', self.gf('django.db.models.fields.IntegerField')()),
            ('orderid', self.gf('django.db.models.fields.IntegerField')()),
            ('dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('email', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['Emails'])

        # Adding model 'Creditcards'
        db.create_table(u'creditcards', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('creditcardtype', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('expiry', self.gf('django.db.models.fields.DateTimeField')()),
            ('dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('customerid', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('legacy', ['Creditcards'])

        # Adding model 'Items'
        db.create_table(u'items', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('serial', self.gf('django.db.models.fields.IntegerField')()),
            ('productid', self.gf('django.db.models.fields.IntegerField')()),
            ('dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('orderid', self.gf('django.db.models.fields.IntegerField')()),
            ('shippingmethod', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('shippingcost', self.gf('django.db.models.fields.FloatField')()),
            ('trackingnum', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dtprocessed', self.gf('django.db.models.fields.DateTimeField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('cost', self.gf('django.db.models.fields.FloatField')()),
            ('linenum', self.gf('django.db.models.fields.IntegerField')()),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
            ('warranty', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('legacy', ['Items'])

        # Adding model 'Issues'
        db.create_table(u'issues', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('customerid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('issue', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('open', self.gf('django.db.models.fields.TextField')()),
            ('dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('consultant', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('emailid', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('legacy', ['Issues'])

        # Adding model 'Itemcomponents'
        db.create_table(u'itemcomponents', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('itemid', self.gf('django.db.models.fields.IntegerField')()),
            ('serial', self.gf('django.db.models.fields.IntegerField')()),
            ('choiceid', self.gf('django.db.models.fields.IntegerField')()),
            ('dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('legacy', ['Itemcomponents'])


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

        # Deleting model 'PgaQueries'
        db.delete_table(u'pga_queries')

        # Deleting model 'PgaForms'
        db.delete_table(u'pga_forms')

        # Deleting model 'PgaScripts'
        db.delete_table(u'pga_scripts')

        # Deleting model 'PgaReports'
        db.delete_table(u'pga_reports')

        # Deleting model 'PgaLayout'
        db.delete_table(u'pga_layout')

        # Deleting model 'PgaGraphs'
        db.delete_table(u'pga_graphs')

        # Deleting model 'PgaImages'
        db.delete_table(u'pga_images')

        # Deleting model 'PgaDiagrams'
        db.delete_table(u'pga_diagrams')

        # Deleting model 'Costspersku'
        db.delete_table(u'costspersku')

        # Deleting model 'Optchoices'
        db.delete_table(u'optchoices')

        # Deleting model 'Optionchoices'
        db.delete_table(u'optionchoices')

        # Deleting model 'ChoiceCategory'
        db.delete_table(u'choicecategories')

        # Deleting model 'Choice'
        db.delete_table(u'choices')

        # Deleting model 'Option'
        db.delete_table(u'options')

        # Deleting model 'Product'
        db.delete_table(u'products')

        # Deleting model 'Categories'
        db.delete_table(u'categories')

        # Deleting model 'Prodopt'
        db.delete_table(u'prodopts')

        # Deleting model 'Prodoptchoice'
        db.delete_table(u'prodoptchoices')

        # Deleting model 'Addresses'
        db.delete_table(u'addresses')

        # Deleting model 'Orders'
        db.delete_table(u'orders')

        # Deleting model 'Emails'
        db.delete_table(u'emails')

        # Deleting model 'Creditcards'
        db.delete_table(u'creditcards')

        # Deleting model 'Items'
        db.delete_table(u'items')

        # Deleting model 'Issues'
        db.delete_table(u'issues')

        # Deleting model 'Itemcomponents'
        db.delete_table(u'itemcomponents')


    models = {
        'legacy.addresses': {
            'Meta': {'object_name': 'Addresses', 'db_table': "u'addresses'"},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'customerid': ('django.db.models.fields.IntegerField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'legacy.cacounties': {
            'Meta': {'object_name': 'Cacounties', 'db_table': "u'cacounties'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.cacountycounts': {
            'Meta': {'object_name': 'Cacountycounts', 'db_table': "u'cacountycounts'"},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.cacountytax': {
            'Meta': {'object_name': 'Cacountytax', 'db_table': "u'cacountytax'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.cacountytaxcounts': {
            'Meta': {'object_name': 'Cacountytaxcounts', 'db_table': "u'cacountytaxcounts'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.catax': {
            'Meta': {'object_name': 'Catax', 'db_table': "u'catax'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.categories': {
            'Meta': {'object_name': 'Categories', 'db_table': "u'categories'"},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'legacy.choice': {
            'Meta': {'ordering': "['sortorder']", 'object_name': 'Choice', 'db_table': "u'choices'"},
            'avehours': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'choicecategory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.ChoiceCategory']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'current': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {}),
            'supplier': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'legacy.choicecategory': {
            'Meta': {'object_name': 'ChoiceCategory', 'db_table': "u'choicecategories'"},
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sohigh': ('django.db.models.fields.IntegerField', [], {}),
            'solow': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.costspersku': {
            'Meta': {'object_name': 'Costspersku', 'db_table': "u'costspersku'"},
            'defaultcost': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'legacy.creditcards': {
            'Meta': {'object_name': 'Creditcards', 'db_table': "u'creditcards'"},
            'creditcardtype': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'customerid': ('django.db.models.fields.IntegerField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'expiry': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.emails': {
            'Meta': {'object_name': 'Emails', 'db_table': "u'emails'"},
            'customerid': ('django.db.models.fields.IntegerField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orderid': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.issues': {
            'Meta': {'object_name': 'Issues', 'db_table': "u'issues'"},
            'consultant': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'customerid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'emailid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'open': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.itemcomponents': {
            'Meta': {'object_name': 'Itemcomponents', 'db_table': "u'itemcomponents'"},
            'choiceid': ('django.db.models.fields.IntegerField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'itemid': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'serial': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.items': {
            'Meta': {'object_name': 'Items', 'db_table': "u'items'"},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'dtprocessed': ('django.db.models.fields.DateTimeField', [], {}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'linenum': ('django.db.models.fields.IntegerField', [], {}),
            'orderid': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'productid': ('django.db.models.fields.IntegerField', [], {}),
            'serial': ('django.db.models.fields.IntegerField', [], {}),
            'shippingcost': ('django.db.models.fields.FloatField', [], {}),
            'shippingmethod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'trackingnum': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'warranty': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'legacy.optchoices': {
            'Meta': {'object_name': 'Optchoices', 'db_table': "u'optchoices'"},
            'choiceid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'optid': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.option': {
            'Meta': {'ordering': "['sortorder']", 'object_name': 'Option', 'db_table': "u'options'"},
            'avehours': ('django.db.models.fields.IntegerField', [], {}),
            'dependencies': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'faq': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.optionchoices': {
            'Meta': {'object_name': 'Optionchoices', 'db_table': "u'optionchoices'"},
            'choiceid': ('django.db.models.fields.IntegerField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'optionid': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.orders': {
            'Meta': {'object_name': 'Orders', 'db_table': "u'orders'"},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'customerid': ('django.db.models.fields.IntegerField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'dtprocessed': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'returned': ('django.db.models.fields.TextField', [], {}),
            'shipping': ('django.db.models.fields.FloatField', [], {}),
            'shippingmethod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.pgadiagrams': {
            'Meta': {'object_name': 'PgaDiagrams', 'db_table': "u'pga_diagrams'"},
            'diagramlinks': ('django.db.models.fields.TextField', [], {}),
            'diagramname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'diagramtables': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.pgaforms': {
            'Meta': {'object_name': 'PgaForms', 'db_table': "u'pga_forms'"},
            'formname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'formsource': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'legacy.pgagraphs': {
            'Meta': {'object_name': 'PgaGraphs', 'db_table': "u'pga_graphs'"},
            'graphcode': ('django.db.models.fields.TextField', [], {}),
            'graphname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'graphsource': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.pgaimages': {
            'Meta': {'object_name': 'PgaImages', 'db_table': "u'pga_images'"},
            'imagename': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'imagesource': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.pgalayout': {
            'Meta': {'object_name': 'PgaLayout', 'db_table': "u'pga_layout'"},
            'colnames': ('django.db.models.fields.TextField', [], {}),
            'colwidth': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nrcols': ('django.db.models.fields.SmallIntegerField', [], {}),
            'tablename': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'legacy.pgaqueries': {
            'Meta': {'object_name': 'PgaQueries', 'db_table': "u'pga_queries'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'querycommand': ('django.db.models.fields.TextField', [], {}),
            'querycomments': ('django.db.models.fields.TextField', [], {}),
            'querylinks': ('django.db.models.fields.TextField', [], {}),
            'queryname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'queryresults': ('django.db.models.fields.TextField', [], {}),
            'querytables': ('django.db.models.fields.TextField', [], {}),
            'querytype': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.pgareports': {
            'Meta': {'object_name': 'PgaReports', 'db_table': "u'pga_reports'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reportbody': ('django.db.models.fields.TextField', [], {}),
            'reportname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'reportoptions': ('django.db.models.fields.TextField', [], {}),
            'reportprocs': ('django.db.models.fields.TextField', [], {}),
            'reportsource': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.pgascripts': {
            'Meta': {'object_name': 'PgaScripts', 'db_table': "u'pga_scripts'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scriptname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'scriptsource': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.prodopt': {
            'Meta': {'object_name': 'Prodopt', 'db_table': "u'prodopts'"},
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'prodopts'", 'symmetrical': 'False', 'through': "orm['legacy.Prodoptchoice']", 'to': "orm['legacy.Choice']"}),
            'defaultchoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Choice']", 'db_column': "'defaultchoiceid'"}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Option']", 'db_column': "'optionid'"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Product']", 'db_column': "'productid'"})
        },
        'legacy.prodoptchoice': {
            'Meta': {'object_name': 'Prodoptchoice', 'db_table': "u'prodoptchoices'"},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Choice']", 'db_column': "'choiceid'"}),
            'current': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pricedelta': ('django.db.models.fields.FloatField', [], {}),
            'productoption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Prodopt']", 'db_column': "'productoptionid'"})
        },
        'legacy.product': {
            'Meta': {'ordering': "['sku']", 'object_name': 'Product', 'db_table': "u'products'"},
            'algorithm': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'baseoptions': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'baseprice': ('django.db.models.fields.FloatField', [], {}),
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Categories']", 'db_column': "'categoryid'"}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'current': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['legacy.Option']", 'through': "orm['legacy.Prodopt']", 'symmetrical': 'False'}),
            'pix': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['legacy']
