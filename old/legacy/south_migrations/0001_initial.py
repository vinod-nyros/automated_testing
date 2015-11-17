# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from django_eracks.apps.legacy.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Catax'
        db.create_table(u'catax', (
            ('id', orm['legacy.Catax:id']),
            ('county', orm['legacy.Catax:county']),
            ('city', orm['legacy.Catax:city']),
            ('tax', orm['legacy.Catax:tax']),
            ('count', orm['legacy.Catax:count']),
        ))
        db.send_create_signal('legacy', ['Catax'])
        
        # Adding model 'Prodoptchoice'
        db.create_table(u'prodoptchoices', (
            ('id', orm['legacy.Prodoptchoice:id']),
            ('dt', orm['legacy.Prodoptchoice:dt']),
            ('pricedelta', orm['legacy.Prodoptchoice:pricedelta']),
            ('productoption', orm['legacy.Prodoptchoice:productoption']),
            ('choice', orm['legacy.Prodoptchoice:choice']),
            ('current', orm['legacy.Prodoptchoice:current']),
        ))
        db.send_create_signal('legacy', ['Prodoptchoice'])
        
        # Adding model 'PgaReports'
        db.create_table(u'pga_reports', (
            ('id', orm['legacy.PgaReports:id']),
            ('reportname', orm['legacy.PgaReports:reportname']),
            ('reportsource', orm['legacy.PgaReports:reportsource']),
            ('reportbody', orm['legacy.PgaReports:reportbody']),
            ('reportprocs', orm['legacy.PgaReports:reportprocs']),
            ('reportoptions', orm['legacy.PgaReports:reportoptions']),
        ))
        db.send_create_signal('legacy', ['PgaReports'])
        
        # Adding model 'Optchoices'
        db.create_table(u'optchoices', (
            ('id', orm['legacy.Optchoices:id']),
            ('optid', orm['legacy.Optchoices:optid']),
            ('choiceid', orm['legacy.Optchoices:choiceid']),
        ))
        db.send_create_signal('legacy', ['Optchoices'])
        
        # Adding model 'PgaImages'
        db.create_table(u'pga_images', (
            ('imagename', orm['legacy.PgaImages:imagename']),
            ('imagesource', orm['legacy.PgaImages:imagesource']),
        ))
        db.send_create_signal('legacy', ['PgaImages'])
        
        # Adding model 'Cacountytax'
        db.create_table(u'cacountytax', (
            ('id', orm['legacy.Cacountytax:id']),
            ('city', orm['legacy.Cacountytax:city']),
            ('tax', orm['legacy.Cacountytax:tax']),
            ('county', orm['legacy.Cacountytax:county']),
        ))
        db.send_create_signal('legacy', ['Cacountytax'])
        
        # Adding model 'Choicecategories'
        db.create_table(u'choicecategories', (
            ('id', orm['legacy.Choicecategories:id']),
            ('dt', orm['legacy.Choicecategories:dt']),
            ('name', orm['legacy.Choicecategories:name']),
            ('sohigh', orm['legacy.Choicecategories:sohigh']),
            ('solow', orm['legacy.Choicecategories:solow']),
        ))
        db.send_create_signal('legacy', ['Choicecategories'])
        
        # Adding model 'Prodopt'
        db.create_table(u'prodopts', (
            ('id', orm['legacy.Prodopt:id']),
            ('dt', orm['legacy.Prodopt:dt']),
            ('product', orm['legacy.Prodopt:product']),
            ('option', orm['legacy.Prodopt:option']),
            ('defaultchoice', orm['legacy.Prodopt:defaultchoice']),
        ))
        db.send_create_signal('legacy', ['Prodopt'])
        
        # Adding model 'PgaScripts'
        db.create_table(u'pga_scripts', (
            ('id', orm['legacy.PgaScripts:id']),
            ('scriptname', orm['legacy.PgaScripts:scriptname']),
            ('scriptsource', orm['legacy.PgaScripts:scriptsource']),
        ))
        db.send_create_signal('legacy', ['PgaScripts'])
        
        # Adding model 'PgaDiagrams'
        db.create_table(u'pga_diagrams', (
            ('diagramname', orm['legacy.PgaDiagrams:diagramname']),
            ('diagramtables', orm['legacy.PgaDiagrams:diagramtables']),
            ('diagramlinks', orm['legacy.PgaDiagrams:diagramlinks']),
        ))
        db.send_create_signal('legacy', ['PgaDiagrams'])
        
        # Adding model 'Customers'
        db.create_table(u'customers', (
            ('id', orm['legacy.Customers:id']),
            ('dt', orm['legacy.Customers:dt']),
            ('name', orm['legacy.Customers:name']),
            ('title', orm['legacy.Customers:title']),
            ('dept', orm['legacy.Customers:dept']),
            ('email', orm['legacy.Customers:email']),
            ('email2', orm['legacy.Customers:email2']),
            ('phone', orm['legacy.Customers:phone']),
            ('phone2', orm['legacy.Customers:phone2']),
            ('maillist', orm['legacy.Customers:maillist']),
            ('primarybilling', orm['legacy.Customers:primarybilling']),
            ('primaryshipping', orm['legacy.Customers:primaryshipping']),
            ('primarycreditcard', orm['legacy.Customers:primarycreditcard']),
            ('comment', orm['legacy.Customers:comment']),
        ))
        db.send_create_signal('legacy', ['Customers'])
        
        # Adding model 'PgaForms'
        db.create_table(u'pga_forms', (
            ('id', orm['legacy.PgaForms:id']),
            ('formname', orm['legacy.PgaForms:formname']),
            ('formsource', orm['legacy.PgaForms:formsource']),
        ))
        db.send_create_signal('legacy', ['PgaForms'])
        
        # Adding model 'Optionchoices'
        db.create_table(u'optionchoices', (
            ('id', orm['legacy.Optionchoices:id']),
            ('dt', orm['legacy.Optionchoices:dt']),
            ('optionid', orm['legacy.Optionchoices:optionid']),
            ('choiceid', orm['legacy.Optionchoices:choiceid']),
            ('comment', orm['legacy.Optionchoices:comment']),
        ))
        db.send_create_signal('legacy', ['Optionchoices'])
        
        # Adding model 'Cacountycounts'
        db.create_table(u'cacountycounts', (
            ('id', orm['legacy.Cacountycounts:id']),
            ('county', orm['legacy.Cacountycounts:county']),
            ('tax', orm['legacy.Cacountycounts:tax']),
            ('count', orm['legacy.Cacountycounts:count']),
        ))
        db.send_create_signal('legacy', ['Cacountycounts'])
        
        # Adding model 'PgaQueries'
        db.create_table(u'pga_queries', (
            ('id', orm['legacy.PgaQueries:id']),
            ('queryname', orm['legacy.PgaQueries:queryname']),
            ('querytype', orm['legacy.PgaQueries:querytype']),
            ('querycommand', orm['legacy.PgaQueries:querycommand']),
            ('querytables', orm['legacy.PgaQueries:querytables']),
            ('querylinks', orm['legacy.PgaQueries:querylinks']),
            ('queryresults', orm['legacy.PgaQueries:queryresults']),
            ('querycomments', orm['legacy.PgaQueries:querycomments']),
        ))
        db.send_create_signal('legacy', ['PgaQueries'])
        
        # Adding model 'Itemcomponents'
        db.create_table(u'itemcomponents', (
            ('id', orm['legacy.Itemcomponents:id']),
            ('itemid', orm['legacy.Itemcomponents:itemid']),
            ('serial', orm['legacy.Itemcomponents:serial']),
            ('choiceid', orm['legacy.Itemcomponents:choiceid']),
            ('dt', orm['legacy.Itemcomponents:dt']),
            ('comment', orm['legacy.Itemcomponents:comment']),
            ('price', orm['legacy.Itemcomponents:price']),
            ('hours', orm['legacy.Itemcomponents:hours']),
        ))
        db.send_create_signal('legacy', ['Itemcomponents'])
        
        # Adding model 'Orders'
        db.create_table(u'orders', (
            ('id', orm['legacy.Orders:id']),
            ('dt', orm['legacy.Orders:dt']),
            ('customerid', orm['legacy.Orders:customerid']),
            ('price', orm['legacy.Orders:price']),
            ('tax', orm['legacy.Orders:tax']),
            ('shipping', orm['legacy.Orders:shipping']),
            ('shippingmethod', orm['legacy.Orders:shippingmethod']),
            ('dtprocessed', orm['legacy.Orders:dtprocessed']),
            ('returned', orm['legacy.Orders:returned']),
            ('comment', orm['legacy.Orders:comment']),
            ('state', orm['legacy.Orders:state']),
        ))
        db.send_create_signal('legacy', ['Orders'])
        
        # Adding model 'Cacountytaxcounts'
        db.create_table(u'cacountytaxcounts', (
            ('id', orm['legacy.Cacountytaxcounts:id']),
            ('county', orm['legacy.Cacountytaxcounts:county']),
            ('city', orm['legacy.Cacountytaxcounts:city']),
            ('tax', orm['legacy.Cacountytaxcounts:tax']),
            ('count', orm['legacy.Cacountytaxcounts:count']),
        ))
        db.send_create_signal('legacy', ['Cacountytaxcounts'])
        
        # Adding model 'PgaGraphs'
        db.create_table(u'pga_graphs', (
            ('graphname', orm['legacy.PgaGraphs:graphname']),
            ('graphsource', orm['legacy.PgaGraphs:graphsource']),
            ('graphcode', orm['legacy.PgaGraphs:graphcode']),
        ))
        db.send_create_signal('legacy', ['PgaGraphs'])
        
        # Adding model 'Cacounties'
        db.create_table(u'cacounties', (
            ('id', orm['legacy.Cacounties:id']),
            ('city', orm['legacy.Cacounties:city']),
            ('tax', orm['legacy.Cacounties:tax']),
            ('county', orm['legacy.Cacounties:county']),
        ))
        db.send_create_signal('legacy', ['Cacounties'])
        
        # Adding model 'Emails'
        db.create_table(u'emails', (
            ('id', orm['legacy.Emails:id']),
            ('customerid', orm['legacy.Emails:customerid']),
            ('orderid', orm['legacy.Emails:orderid']),
            ('dt', orm['legacy.Emails:dt']),
            ('email', orm['legacy.Emails:email']),
        ))
        db.send_create_signal('legacy', ['Emails'])
        
        # Adding model 'Creditcards'
        db.create_table(u'creditcards', (
            ('id', orm['legacy.Creditcards:id']),
            ('name', orm['legacy.Creditcards:name']),
            ('creditcardtype', orm['legacy.Creditcards:creditcardtype']),
            ('number', orm['legacy.Creditcards:number']),
            ('expiry', orm['legacy.Creditcards:expiry']),
            ('dt', orm['legacy.Creditcards:dt']),
            ('customerid', orm['legacy.Creditcards:customerid']),
        ))
        db.send_create_signal('legacy', ['Creditcards'])
        
        # Adding model 'Categories'
        db.create_table(u'categories', (
            ('id', orm['legacy.Categories:id']),
            ('name', orm['legacy.Categories:name']),
            ('dt', orm['legacy.Categories:dt']),
            ('blurb', orm['legacy.Categories:blurb']),
        ))
        db.send_create_signal('legacy', ['Categories'])
        
        # Adding model 'Option'
        db.create_table(u'options', (
            ('id', orm['legacy.Option:id']),
            ('name', orm['legacy.Option:name']),
            ('dt', orm['legacy.Option:dt']),
            ('dependencies', orm['legacy.Option:dependencies']),
            ('avehours', orm['legacy.Option:avehours']),
            ('faq', orm['legacy.Option:faq']),
            ('sortorder', orm['legacy.Option:sortorder']),
        ))
        db.send_create_signal('legacy', ['Option'])
        
        # Adding model 'Choice'
        db.create_table(u'choices', (
            ('id', orm['legacy.Choice:id']),
            ('dt', orm['legacy.Choice:dt']),
            ('current', orm['legacy.Choice:current']),
            ('name', orm['legacy.Choice:name']),
            ('supplier', orm['legacy.Choice:supplier']),
            ('price', orm['legacy.Choice:price']),
            ('cost', orm['legacy.Choice:cost']),
            ('avehours', orm['legacy.Choice:avehours']),
            ('sortorder', orm['legacy.Choice:sortorder']),
            ('multiplier', orm['legacy.Choice:multiplier']),
            ('comment', orm['legacy.Choice:comment']),
        ))
        db.send_create_signal('legacy', ['Choice'])
        
        # Adding model 'Addresses'
        db.create_table(u'addresses', (
            ('id', orm['legacy.Addresses:id']),
            ('customerid', orm['legacy.Addresses:customerid']),
            ('address1', orm['legacy.Addresses:address1']),
            ('address2', orm['legacy.Addresses:address2']),
            ('name', orm['legacy.Addresses:name']),
            ('city', orm['legacy.Addresses:city']),
            ('state', orm['legacy.Addresses:state']),
            ('zip', orm['legacy.Addresses:zip']),
            ('country', orm['legacy.Addresses:country']),
            ('phone', orm['legacy.Addresses:phone']),
            ('email', orm['legacy.Addresses:email']),
            ('type', orm['legacy.Addresses:type']),
            ('dt', orm['legacy.Addresses:dt']),
        ))
        db.send_create_signal('legacy', ['Addresses'])
        
        # Adding model 'Product'
        db.create_table(u'products', (
            ('id', orm['legacy.Product:id']),
            ('name', orm['legacy.Product:name']),
            ('sku', orm['legacy.Product:sku']),
            ('baseprice', orm['legacy.Product:baseprice']),
            ('cost', orm['legacy.Product:cost']),
            ('category', orm['legacy.Product:category']),
            ('pix', orm['legacy.Product:pix']),
            ('baseoptions', orm['legacy.Product:baseoptions']),
            ('dt', orm['legacy.Product:dt']),
            ('current', orm['legacy.Product:current']),
            ('blurb', orm['legacy.Product:blurb']),
            ('algorithm', orm['legacy.Product:algorithm']),
            ('sortorder', orm['legacy.Product:sortorder']),
            ('multiplier', orm['legacy.Product:multiplier']),
            ('weight', orm['legacy.Product:weight']),
            ('description', orm['legacy.Product:description']),
            ('link', orm['legacy.Product:link']),
            ('image', orm['legacy.Product:image']),
            ('title', orm['legacy.Product:title']),
        ))
        db.send_create_signal('legacy', ['Product'])
        
        # Adding model 'Issues'
        db.create_table(u'issues', (
            ('id', orm['legacy.Issues:id']),
            ('customerid', orm['legacy.Issues:customerid']),
            ('issue', orm['legacy.Issues:issue']),
            ('open', orm['legacy.Issues:open']),
            ('dt', orm['legacy.Issues:dt']),
            ('consultant', orm['legacy.Issues:consultant']),
            ('emailid', orm['legacy.Issues:emailid']),
        ))
        db.send_create_signal('legacy', ['Issues'])
        
        # Adding model 'Costspersku'
        db.create_table(u'costspersku', (
            ('id', orm['legacy.Costspersku:id']),
            ('sku', orm['legacy.Costspersku:sku']),
            ('defaultcost', orm['legacy.Costspersku:defaultcost']),
        ))
        db.send_create_signal('legacy', ['Costspersku'])
        
        # Adding model 'PgaLayout'
        db.create_table(u'pga_layout', (
            ('id', orm['legacy.PgaLayout:id']),
            ('tablename', orm['legacy.PgaLayout:tablename']),
            ('nrcols', orm['legacy.PgaLayout:nrcols']),
            ('colnames', orm['legacy.PgaLayout:colnames']),
            ('colwidth', orm['legacy.PgaLayout:colwidth']),
        ))
        db.send_create_signal('legacy', ['PgaLayout'])
        
        # Adding model 'Items'
        db.create_table(u'items', (
            ('id', orm['legacy.Items:id']),
            ('serial', orm['legacy.Items:serial']),
            ('productid', orm['legacy.Items:productid']),
            ('dt', orm['legacy.Items:dt']),
            ('orderid', orm['legacy.Items:orderid']),
            ('shippingmethod', orm['legacy.Items:shippingmethod']),
            ('shippingcost', orm['legacy.Items:shippingcost']),
            ('trackingnum', orm['legacy.Items:trackingnum']),
            ('dtprocessed', orm['legacy.Items:dtprocessed']),
            ('state', orm['legacy.Items:state']),
            ('price', orm['legacy.Items:price']),
            ('cost', orm['legacy.Items:cost']),
            ('linenum', orm['legacy.Items:linenum']),
            ('hours', orm['legacy.Items:hours']),
            ('warranty', orm['legacy.Items:warranty']),
            ('comment', orm['legacy.Items:comment']),
        ))
        db.send_create_signal('legacy', ['Items'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Catax'
        db.delete_table(u'catax')
        
        # Deleting model 'Prodoptchoice'
        db.delete_table(u'prodoptchoices')
        
        # Deleting model 'PgaReports'
        db.delete_table(u'pga_reports')
        
        # Deleting model 'Optchoices'
        db.delete_table(u'optchoices')
        
        # Deleting model 'PgaImages'
        db.delete_table(u'pga_images')
        
        # Deleting model 'Cacountytax'
        db.delete_table(u'cacountytax')
        
        # Deleting model 'Choicecategories'
        db.delete_table(u'choicecategories')
        
        # Deleting model 'Prodopt'
        db.delete_table(u'prodopts')
        
        # Deleting model 'PgaScripts'
        db.delete_table(u'pga_scripts')
        
        # Deleting model 'PgaDiagrams'
        db.delete_table(u'pga_diagrams')
        
        # Deleting model 'Customers'
        db.delete_table(u'customers')
        
        # Deleting model 'PgaForms'
        db.delete_table(u'pga_forms')
        
        # Deleting model 'Optionchoices'
        db.delete_table(u'optionchoices')
        
        # Deleting model 'Cacountycounts'
        db.delete_table(u'cacountycounts')
        
        # Deleting model 'PgaQueries'
        db.delete_table(u'pga_queries')
        
        # Deleting model 'Itemcomponents'
        db.delete_table(u'itemcomponents')
        
        # Deleting model 'Orders'
        db.delete_table(u'orders')
        
        # Deleting model 'Cacountytaxcounts'
        db.delete_table(u'cacountytaxcounts')
        
        # Deleting model 'PgaGraphs'
        db.delete_table(u'pga_graphs')
        
        # Deleting model 'Cacounties'
        db.delete_table(u'cacounties')
        
        # Deleting model 'Emails'
        db.delete_table(u'emails')
        
        # Deleting model 'Creditcards'
        db.delete_table(u'creditcards')
        
        # Deleting model 'Categories'
        db.delete_table(u'categories')
        
        # Deleting model 'Option'
        db.delete_table(u'options')
        
        # Deleting model 'Choice'
        db.delete_table(u'choices')
        
        # Deleting model 'Addresses'
        db.delete_table(u'addresses')
        
        # Deleting model 'Product'
        db.delete_table(u'products')
        
        # Deleting model 'Issues'
        db.delete_table(u'issues')
        
        # Deleting model 'Costspersku'
        db.delete_table(u'costspersku')
        
        # Deleting model 'PgaLayout'
        db.delete_table(u'pga_layout')
        
        # Deleting model 'Items'
        db.delete_table(u'items')
        
    
    
    models = {
        'legacy.addresses': {
            'Meta': {'db_table': "u'addresses'"},
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
            'Meta': {'db_table': "u'cacounties'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '-1'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '-1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.cacountycounts': {
            'Meta': {'db_table': "u'cacountycounts'"},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '-1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.cacountytax': {
            'Meta': {'db_table': "u'cacountytax'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '-1'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '-1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.cacountytaxcounts': {
            'Meta': {'db_table': "u'cacountytaxcounts'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '-1'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '-1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.catax': {
            'Meta': {'db_table': "u'catax'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '-1'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '-1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        'legacy.categories': {
            'Meta': {'db_table': "u'categories'"},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'legacy.choice': {
            'Meta': {'db_table': "u'choices'"},
            'avehours': ('django.db.models.fields.IntegerField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'current': ('django.db.models.fields.TextField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {}),
            'supplier': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.choicecategories': {
            'Meta': {'db_table': "u'choicecategories'"},
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sohigh': ('django.db.models.fields.IntegerField', [], {}),
            'solow': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.costspersku': {
            'Meta': {'db_table': "u'costspersku'"},
            'defaultcost': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'legacy.creditcards': {
            'Meta': {'db_table': "u'creditcards'"},
            'creditcardtype': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'customerid': ('django.db.models.fields.IntegerField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'expiry': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.customers': {
            'Meta': {'db_table': "u'customers'"},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'dept': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'maillist': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'primarybilling': ('django.db.models.fields.IntegerField', [], {}),
            'primarycreditcard': ('django.db.models.fields.IntegerField', [], {}),
            'primaryshipping': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'legacy.emails': {
            'Meta': {'db_table': "u'emails'"},
            'customerid': ('django.db.models.fields.IntegerField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'orderid': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.issues': {
            'Meta': {'db_table': "u'issues'"},
            'consultant': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'customerid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'emailid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'open': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.itemcomponents': {
            'Meta': {'db_table': "u'itemcomponents'"},
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
            'Meta': {'db_table': "u'items'"},
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
            'Meta': {'db_table': "u'optchoices'"},
            'choiceid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'optid': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.option': {
            'Meta': {'db_table': "u'options'"},
            'avehours': ('django.db.models.fields.IntegerField', [], {}),
            'dependencies': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'faq': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.optionchoices': {
            'Meta': {'db_table': "u'optionchoices'"},
            'choiceid': ('django.db.models.fields.IntegerField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'optionid': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.orders': {
            'Meta': {'db_table': "u'orders'"},
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
            'Meta': {'db_table': "u'pga_diagrams'"},
            'diagramlinks': ('django.db.models.fields.TextField', [], {}),
            'diagramname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'diagramtables': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.pgaforms': {
            'Meta': {'db_table': "u'pga_forms'"},
            'formname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'formsource': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'legacy.pgagraphs': {
            'Meta': {'db_table': "u'pga_graphs'"},
            'graphcode': ('django.db.models.fields.TextField', [], {}),
            'graphname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'graphsource': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.pgaimages': {
            'Meta': {'db_table': "u'pga_images'"},
            'imagename': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'imagesource': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.pgalayout': {
            'Meta': {'db_table': "u'pga_layout'"},
            'colnames': ('django.db.models.fields.TextField', [], {}),
            'colwidth': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nrcols': ('django.db.models.fields.SmallIntegerField', [], {}),
            'tablename': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'legacy.pgaqueries': {
            'Meta': {'db_table': "u'pga_queries'"},
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
            'Meta': {'db_table': "u'pga_reports'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reportbody': ('django.db.models.fields.TextField', [], {}),
            'reportname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'reportoptions': ('django.db.models.fields.TextField', [], {}),
            'reportprocs': ('django.db.models.fields.TextField', [], {}),
            'reportsource': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.pgascripts': {
            'Meta': {'db_table': "u'pga_scripts'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scriptname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'scriptsource': ('django.db.models.fields.TextField', [], {})
        },
        'legacy.prodopt': {
            'Meta': {'db_table': "u'prodopts'"},
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['legacy.Choice']"}),
            'defaultchoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Choice']", 'db_column': "'defaultchoiceid'"}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Option']", 'db_column': "'optionid'"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Product']", 'db_column': "'productid'"})
        },
        'legacy.prodoptchoice': {
            'Meta': {'db_table': "u'prodoptchoices'"},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Choice']", 'db_column': "'choiceid'"}),
            'current': ('django.db.models.fields.TextField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'pricedelta': ('django.db.models.fields.FloatField', [], {}),
            'productoption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Prodopt']", 'db_column': "'productoptionid'"})
        },
        'legacy.product': {
            'Meta': {'db_table': "u'products'"},
            'algorithm': ('django.db.models.fields.TextField', [], {}),
            'baseoptions': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'baseprice': ('django.db.models.fields.FloatField', [], {}),
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Categories']", 'db_column': "'categoryid'"}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'current': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['legacy.Option']"}),
            'pix': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        }
    }
    
    complete_apps = ['legacy']
