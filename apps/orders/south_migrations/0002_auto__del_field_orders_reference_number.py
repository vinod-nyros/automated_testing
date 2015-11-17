# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Orders.reference_number'
        db.delete_column(u'orders', 'reference_number')


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Orders.reference_number'
        raise RuntimeError("Cannot reverse this migration. 'Orders.reference_number' and its values cannot be restored.")


    models = {
        'customers.customer': {
            'Meta': {'object_name': 'Customer', 'db_table': "u'customers'"},
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
        'orders.orders': {
            'Meta': {'object_name': 'Orders', 'db_table': "u'orders'"},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preferred_shipper': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'processed': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'referral_source': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'referral_type': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'shipping': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'shipping_method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shipping_payment': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'special_instructions': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['orders']
