# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
#from django_eracks.apps.quotes.models import *

class Migration:

    def forwards(self, orm):

        # Changing field 'Customer.billing_address'
        # (to signature: django.db.models.fields.TextField(blank=True))
        db.alter_column(u'customers', 'billing_address', orm['quotes.customer:billing_address'])

        # Changing field 'Customer.phone2'
        # (to signature: django.db.models.fields.CharField(max_length=40, blank=True))
        db.alter_column(u'customers', 'phone2', orm['quotes.customer:phone2'])

        # Changing field 'Customer.dept'
        # (to signature: django.db.models.fields.CharField(max_length=80, blank=True))
        db.alter_column(u'customers', 'dept', orm['quotes.customer:dept'])

        # Changing field 'Customer.title'
        # (to signature: django.db.models.fields.CharField(max_length=80, blank=True))
        db.alter_column(u'customers', 'title', orm['quotes.customer:title'])

        # Changing field 'Customer.email2'
        # (to signature: django.db.models.fields.CharField(max_length=160, blank=True))
        db.alter_column(u'customers', 'email2', orm['quotes.customer:email2'])



    def backwards(self, orm):

        # Changing field 'Customer.billing_address'
        # (to signature: django.db.models.fields.TextField())
        db.alter_column(u'customers', 'billing_address', orm['quotes.customer:billing_address'])

        # Changing field 'Customer.phone2'
        # (to signature: django.db.models.fields.CharField(max_length=40))
        db.alter_column(u'customers', 'phone2', orm['quotes.customer:phone2'])

        # Changing field 'Customer.dept'
        # (to signature: django.db.models.fields.CharField(max_length=80))
        db.alter_column(u'customers', 'dept', orm['quotes.customer:dept'])

        # Changing field 'Customer.title'
        # (to signature: django.db.models.fields.CharField(max_length=80))
        db.alter_column(u'customers', 'title', orm['quotes.customer:title'])

        # Changing field 'Customer.email2'
        # (to signature: django.db.models.fields.CharField(max_length=160))
        db.alter_column(u'customers', 'email2', orm['quotes.customer:email2'])



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
            'billing_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dept': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'email2': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maillist': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'primarybilling': ('django.db.models.fields.IntegerField', [], {}),
            'primarycreditcard': ('django.db.models.fields.IntegerField', [], {}),
            'primaryshipping': ('django.db.models.fields.IntegerField', [], {}),
            'shipping_address': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
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
