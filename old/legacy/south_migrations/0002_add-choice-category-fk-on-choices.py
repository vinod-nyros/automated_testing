# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from django_eracks.apps.legacy.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Choice.choicecategory'
        db.add_column(u'choices', 'choicecategory', orm['legacy.Choice:choicecategory'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Choice.choicecategory'
        db.delete_column(u'choices', 'choicecategory_id')
        
    
    
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
            'choicecategory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.ChoiceCategory']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'current': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {}),
            'supplier': ('django.db.models.fields.IntegerField', [], {})
        },
        'legacy.choicecategory': {
            'Meta': {'db_table': "u'choicecategories'"},
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Option']", 'db_column': "'optionid'"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Product']", 'db_column': "'productid'"})
        },
        'legacy.prodoptchoice': {
            'Meta': {'db_table': "u'prodoptchoices'"},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Choice']", 'db_column': "'choiceid'"}),
            'current': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
