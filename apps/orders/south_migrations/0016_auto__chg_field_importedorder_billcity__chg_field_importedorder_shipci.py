# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ImportedOrder.billcity'
        db.alter_column('orders_importedorder', 'billcity', self.gf('django.db.models.fields.CharField')(max_length=40))

        # Changing field 'ImportedOrder.shipcity'
        db.alter_column('orders_importedorder', 'shipcity', self.gf('django.db.models.fields.CharField')(max_length=40))


    def backwards(self, orm):
        
        # Changing field 'ImportedOrder.billcity'
        db.alter_column('orders_importedorder', 'billcity', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'ImportedOrder.shipcity'
        db.alter_column('orders_importedorder', 'shipcity', self.gf('django.db.models.fields.CharField')(max_length=30))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 19, 19, 19, 42, 774448)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 19, 19, 19, 42, 774251)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer', 'db_table': "u'customers'"},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'email2': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'orders.importedorder': {
            'Meta': {'object_name': 'ImportedOrder'},
            'adjustamt': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'adjustments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'approved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'billaddr1': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'billaddr2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'billcity': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'billcountry': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'billemail': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'billfax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'billinitials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'billname': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'billorg': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'billphone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'billregn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'billsame': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'billstate': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'billtype': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'billzip': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'cc_charged_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cc_corp_pin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cc_cvv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'cc_initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'ccauthnum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cclast4': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'ccmonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ccyear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'costofgoods': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'iagree': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instr': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'internalnotes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'oldnotes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'orderdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ordernum': ('django.db.models.fields.IntegerField', [], {}),
            'orderstatus': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'payinitials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'paymeth': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'payterms': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'refnum': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'refsrc': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reftyp': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'saleinitials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'salestax': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'shipacct': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'shipaddr1': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'shipaddr2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'shipcity': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'shipcost': ('django.db.models.fields.FloatField', [], {}),
            'shipcountry': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'shipdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shipincl': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'shipinitials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'shipmethod': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'shipname': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'shiporg': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'shippay': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'shipper': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'shipphone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'shipprice': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'shiprate': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'shipregn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'shipstate': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'shiptype': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'shipzip': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'taxcounty': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'taxrate': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tracknumbers': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'orders.order': {
            'Meta': {'object_name': 'Order', 'db_table': "u'orders'"},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preferred_shipper': ('django.db.models.fields.CharField', [], {'default': "'No Preference'", 'max_length': '50'}),
            'processed': ('django.db.models.fields.DateTimeField', [], {}),
            'reference_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'referral_source': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'referral_type': ('django.db.models.fields.CharField', [], {'default': "'Please Select'", 'max_length': '80'}),
            'shipping': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'shipping_method': ('django.db.models.fields.CharField', [], {'default': "'ground'", 'max_length': '50'}),
            'shipping_payment': ('django.db.models.fields.CharField', [], {'default': "'included'", 'max_length': '80'}),
            'special_instructions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['orders']
