# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from quotes.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'QuoteLineItem'
        db.create_table('quotes_quotelineitem', (
            ('id', orm['quotes.QuoteLineItem:id']),
            ('quote', orm['quotes.QuoteLineItem:quote']),
            ('model', orm['quotes.QuoteLineItem:model']),
            ('quantity', orm['quotes.QuoteLineItem:quantity']),
            ('description', orm['quotes.QuoteLineItem:description']),
            ('cost', orm['quotes.QuoteLineItem:cost']),
            ('price', orm['quotes.QuoteLineItem:price']),
            ('created', orm['quotes.QuoteLineItem:created']),
            ('modified', orm['quotes.QuoteLineItem:modified']),
        ))
        db.send_create_signal('quotes', ['QuoteLineItem'])

        # Adding model 'Quote'
        db.create_table('quotes_quote', (
            ('id', orm['quotes.Quote:id']),
            ('customer', orm['quotes.Quote:customer']),
            ('quote_number', orm['quotes.Quote:quote_number']),
            ('approved_by', orm['quotes.Quote:approved_by']),
            ('valid_for', orm['quotes.Quote:valid_for']),
            ('purchase_order', orm['quotes.Quote:purchase_order']),
            ('customer_reference', orm['quotes.Quote:customer_reference']),
            ('terms', orm['quotes.Quote:terms']),
            ('discount', orm['quotes.Quote:discount']),
            ('discount_type', orm['quotes.Quote:discount_type']),
            ('shipping', orm['quotes.Quote:shipping']),
            ('shipping_method', orm['quotes.Quote:shipping_method']),
            ('target', orm['quotes.Quote:target']),
            ('created', orm['quotes.Quote:created']),
            ('modified', orm['quotes.Quote:modified']),
        ))
        db.send_create_signal('quotes', ['Quote'])



    def backwards(self, orm):

        # Deleting model 'QuoteLineItem'
        db.delete_table('quotes_quotelineitem')

        # Deleting model 'Quote'
        db.delete_table('quotes_quote')



    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'legacy.customer': {
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
        'quotes.quote': {
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Customer']", 'null': 'True'}),
            'customer_reference': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'discount': ('django.db.models.fields.FloatField', [], {}),
            'discount_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'purchase_order': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'quote_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'shipping': ('django.db.models.fields.FloatField', [], {}),
            'shipping_method': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'target': ('django.db.models.fields.FloatField', [], {}),
            'terms': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'valid_for': ('django.db.models.fields.IntegerField', [], {})
        },
        'quotes.quotelineitem': {
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'quote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quotes.Quote']"})
        }
    }

    complete_apps = ['quotes']
