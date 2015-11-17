# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Deleting field 'Orders.dt'
        db.delete_column(u'orders', 'dt')

        # Deleting field 'Orders.dtprocessed'
        db.delete_column(u'orders', 'dtprocessed')

        # Deleting field 'Orders.customerid'
        db.delete_column(u'orders', 'customerid')

        # Adding field 'Orders.customer'
        db.add_column(u'orders', 'customer', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['customers.Customer']), keep_default=False)

        # Adding field 'Orders.created'
        db.add_column(u'orders', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True), keep_default=False)

        # Adding field 'Orders.updated'
        db.add_column(u'orders', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True), keep_default=False)

        # Adding field 'Orders.processed'
        db.add_column(u'orders', 'processed', self.gf('django.db.models.fields.DateTimeField')(), keep_default=False)

        # Adding field 'Orders.published'
        db.add_column(u'orders', 'published', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Changing field 'Orders.id'
        db.alter_column(u'orders', 'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Orders.dt'
        raise RuntimeError("Cannot reverse this migration. 'Orders.dt' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Orders.dtprocessed'
        raise RuntimeError("Cannot reverse this migration. 'Orders.dtprocessed' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Orders.customerid'
        raise RuntimeError("Cannot reverse this migration. 'Orders.customerid' and its values cannot be restored.")

        # Deleting field 'Orders.customer'
        db.delete_column(u'orders', 'customer_id')

        # Deleting field 'Orders.created'
        db.delete_column(u'orders', 'created')

        # Deleting field 'Orders.updated'
        db.delete_column(u'orders', 'updated')

        # Deleting field 'Orders.processed'
        db.delete_column(u'orders', 'processed')

        # Deleting field 'Orders.published'
        db.delete_column(u'orders', 'published')

        # Changing field 'Orders.id'
        db.alter_column(u'orders', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))


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
        'legacy.addresses': {
            'Meta': {'object_name': 'Addresses', 'db_table': "u'addresses'"},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customerid': ('django.db.models.fields.IntegerField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'legacy.choice': {
            'Meta': {'ordering': "['sortorder']", 'object_name': 'Choice', 'db_table': "u'choices'"},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'choicecategory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.ChoiceCategory']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'published': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {}),
            'supplier': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'legacy.choicecategory': {
            'Meta': {'object_name': 'ChoiceCategory', 'db_table': "u'choicecategories'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sohigh': ('django.db.models.fields.IntegerField', [], {}),
            'solow': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'options'", 'symmetrical': 'False', 'to': "orm['legacy.Choice']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage_notes': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        'legacy.orders': {
            'Meta': {'object_name': 'Orders', 'db_table': "u'orders'"},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'processed': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'returned': ('django.db.models.fields.TextField', [], {}),
            'shipping': ('django.db.models.fields.FloatField', [], {}),
            'shippingmethod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tax': ('django.db.models.fields.FloatField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'legacy.prodopt': {
            'Meta': {'object_name': 'Prodopt', 'db_table': "u'prodopts'"},
            'allowed_quantities': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '80', 'blank': 'True'}),
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'prodopts'", 'blank': 'True', 'through': "orm['legacy.Prodoptchoice']", 'to': "orm['legacy.Choice']"}),
            'choices_orderby': ('django.db.models.fields.CharField', [], {'default': "'cost'", 'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'defaultchoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Choice']", 'db_column': "'defaultchoiceid'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Option']", 'db_column': "'optionid'"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Product']", 'db_column': "'productid'"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'qty': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'single': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'legacy.prodoptchoice': {
            'Meta': {'object_name': 'Prodoptchoice', 'db_table': "u'prodoptchoices'"},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Choice']", 'db_column': "'choiceid'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pricedelta': ('django.db.models.fields.FloatField', [], {}),
            'productoption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Prodopt']", 'db_column': "'productoptionid'"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'legacy.product': {
            'Meta': {'ordering': "['sku']", 'object_name': 'Product', 'db_table': "u'products'"},
            'baseoptions': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'baseprice': ('django.db.models.fields.FloatField', [], {}),
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['legacy.Categories']", 'db_column': "'categoryid'"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'features': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'new_grid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['legacy.Option']", 'through': "orm['legacy.Prodopt']", 'symmetrical': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '40'})
        }
    }

    complete_apps = ['legacy']
