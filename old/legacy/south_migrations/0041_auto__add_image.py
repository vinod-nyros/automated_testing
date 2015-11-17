# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('legacy_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('legacy', ['Image'])

        # Adding M2M table for field images on 'Categories'
        db.create_table(u'categories_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('categories', models.ForeignKey(orm['legacy.categories'], null=False)),
            ('image', models.ForeignKey(orm['legacy.image'], null=False))
        ))
        db.create_unique(u'categories_images', ['categories_id', 'image_id'])

        # Adding M2M table for field images on 'Product'
        db.create_table(u'products_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['legacy.product'], null=False)),
            ('image', models.ForeignKey(orm['legacy.image'], null=False))
        ))
        db.create_unique(u'products_images', ['product_id', 'image_id'])


    def backwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('legacy_image')

        # Removing M2M table for field images on 'Categories'
        db.delete_table('categories_images')

        # Removing M2M table for field images on 'Product'
        db.delete_table('products_images')


    models = {
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
        'legacy.categories': {
            'Meta': {'object_name': 'Categories', 'db_table': "u'categories'"},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['legacy.Image']", 'symmetrical': 'False'}),
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
        'legacy.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['legacy.Image']", 'symmetrical': 'False'}),
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
