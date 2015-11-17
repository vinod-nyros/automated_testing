# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
#from django_eracks.apps.quotes.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'Customer'
        db.create_table(u'customers', (
            ('id', orm['quotes.customer:id']),
            ('name', orm['quotes.customer:name']),
            ('title', orm['quotes.customer:title']),
            ('dept', orm['quotes.customer:dept']),
            ('email', orm['quotes.customer:email']),
            ('email2', orm['quotes.customer:email2']),
            ('phone', orm['quotes.customer:phone']),
            ('phone2', orm['quotes.customer:phone2']),
            ('maillist', orm['quotes.customer:maillist']),
            ('primarybilling', orm['quotes.customer:primarybilling']),
            ('primaryshipping', orm['quotes.customer:primaryshipping']),
            ('primarycreditcard', orm['quotes.customer:primarycreditcard']),
            ('comment', orm['quotes.customer:comment']),
            ('dt', orm['quotes.customer:dt']),
        ))
        db.send_create_signal('quotes', ['Customer'])

        # Changing field 'Quote.customer'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['quotes.Customer'], null=True, blank=True))
        db.alter_column('quotes_quote', 'customer_id', orm['quotes.quote:customer'])

        # Changing field 'Quote.shipping_method'
        # (to signature: django.db.models.fields.CharField(max_length=40, blank=True))
        db.alter_column('quotes_quote', 'shipping_method', orm['quotes.quote:shipping_method'])

        # Changing field 'Quote.discount_type'
        # (to signature: django.db.models.fields.CharField(max_length=1, blank=True))
        db.alter_column('quotes_quote', 'discount_type', orm['quotes.quote:discount_type'])

        # Changing field 'Quote.shipping'
        # (to signature: django.db.models.fields.FloatField(blank=True))
        db.alter_column('quotes_quote', 'shipping', orm['quotes.quote:shipping'])

        # Changing field 'Quote.discount'
        # (to signature: django.db.models.fields.FloatField(blank=True))
        db.alter_column('quotes_quote', 'discount', orm['quotes.quote:discount'])

        # Changing field 'Quote.purchase_order'
        # (to signature: django.db.models.fields.CharField(max_length=20, blank=True))
        db.alter_column('quotes_quote', 'purchase_order', orm['quotes.quote:purchase_order'])

        # Changing field 'Quote.customer_reference'
        # (to signature: django.db.models.fields.CharField(max_length=30, blank=True))
        db.alter_column('quotes_quote', 'customer_reference', orm['quotes.quote:customer_reference'])



    def backwards(self, orm):

        # Deleting model 'Customer'
        db.delete_table(u'customers')

        # Changing field 'Quote.customer'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['legacy.Customer'], null=True))
        db.alter_column('quotes_quote', 'customer_id', orm['quotes.quote:customer'])

        # Changing field 'Quote.shipping_method'
        # (to signature: django.db.models.fields.CharField(max_length=40))
        db.alter_column('quotes_quote', 'shipping_method', orm['quotes.quote:shipping_method'])

        # Changing field 'Quote.discount_type'
        # (to signature: django.db.models.fields.CharField(max_length=1))
        db.alter_column('quotes_quote', 'discount_type', orm['quotes.quote:discount_type'])

        # Changing field 'Quote.shipping'
        # (to signature: django.db.models.fields.FloatField())
        db.alter_column('quotes_quote', 'shipping', orm['quotes.quote:shipping'])

        # Changing field 'Quote.discount'
        # (to signature: django.db.models.fields.FloatField())
        db.alter_column('quotes_quote', 'discount', orm['quotes.quote:discount'])

        # Changing field 'Quote.purchase_order'
        # (to signature: django.db.models.fields.CharField(max_length=20))
        db.alter_column('quotes_quote', 'purchase_order', orm['quotes.quote:purchase_order'])

        # Changing field 'Quote.customer_reference'
        # (to signature: django.db.models.fields.CharField(max_length=30))
        db.alter_column('quotes_quote', 'customer_reference', orm['quotes.quote:customer_reference'])



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
            'comment': ('django.db.models.fields.TextField', [], {}),
            'dept': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
