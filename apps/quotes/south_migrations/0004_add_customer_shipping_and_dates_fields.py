# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
#from django_eracks.apps.quotes.models import *

class Migration:

    def forwards(self, orm):

        # Adding field 'Customer.billing_address'
        db.add_column(u'customers', 'billing_address', orm['quotes.customer:billing_address'])

        # Adding field 'Customer.modified'
        db.add_column(u'customers', 'modified', orm['quotes.customer:modified'])

        # Adding field 'Customer.shipping_address'
        db.add_column(u'customers', 'shipping_address', orm['quotes.customer:shipping_address'])

        # Adding field 'Customer.created'
        db.add_column(u'customers', 'created', orm['quotes.customer:created'])

        # Deleting field 'Customer.dt'
        db.delete_column(u'customers', 'dt')



    def backwards(self, orm):

        # Deleting field 'Customer.billing_address'
        db.delete_column(u'customers', 'billing_address')

        # Deleting field 'Customer.modified'
        db.delete_column(u'customers', 'modified')

        # Deleting field 'Customer.shipping_address'
        db.delete_column(u'customers', 'shipping_address')

        # Deleting field 'Customer.created'
        db.delete_column(u'customers', 'created')

        # Adding field 'Customer.dt'
        db.add_column(u'customers', 'dt', orm['quotes.customer:dt'])



    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'quotes.customer': {
            'Meta': {'db_table': "u'customers'"},
            'billing_address': ('django.db.models.fields.TextField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dept': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'email2': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maillist': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'primarybilling': ('django.db.models.fields.IntegerField', [], {}),
            'primarycreditcard': ('django.db.models.fields.IntegerField', [], {}),
            'primaryshipping': ('django.db.models.fields.IntegerField', [], {}),
            'shipping_address': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'quotes.quote': {
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quotes.Customer']", 'null': 'True', 'blank': 'True'}),
            'customer_reference': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'discount': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'discount_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'purchase_order': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'quote_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'shipping': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'shipping_method': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
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
