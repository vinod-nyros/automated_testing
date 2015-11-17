# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('products_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('products', ['Image'])

        # Adding model 'Categories'
        db.create_table(u'categories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('sortorder', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('products', ['Categories'])

        # Adding M2M table for field images on 'Categories'
        db.create_table(u'categories_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('categories', models.ForeignKey(orm['products.categories'], null=False)),
            ('image', models.ForeignKey(orm['products.image'], null=False))
        ))
        db.create_unique(u'categories_images', ['categories_id', 'image_id'])

        # Adding model 'ChoiceCategory'
        db.create_table(u'choicecategories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sohigh', self.gf('django.db.models.fields.IntegerField')()),
            ('solow', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('products', ['ChoiceCategory'])

        # Adding model 'Choice'
        db.create_table(u'choices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('supplier', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('cost', self.gf('django.db.models.fields.FloatField')()),
            ('sortorder', self.gf('django.db.models.fields.IntegerField')()),
            ('multiplier', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('choicecategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.ChoiceCategory'])),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
        ))
        db.send_create_signal('products', ['Choice'])

        # Adding model 'Option'
        db.create_table(u'options', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('usage_notes', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('sortorder', self.gf('django.db.models.fields.IntegerField')()),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('products', ['Option'])

        # Adding M2M table for field choices on 'Option'
        db.create_table(u'options_choices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('option', models.ForeignKey(orm['products.option'], null=False)),
            ('choice', models.ForeignKey(orm['products.choice'], null=False))
        ))
        db.create_unique(u'options_choices', ['option_id', 'choice_id'])

        # Adding model 'Product'
        db.create_table(u'products', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sku', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('baseprice', self.gf('django.db.models.fields.FloatField')()),
            ('cost', self.gf('django.db.models.fields.FloatField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Categories'], db_column='categoryid')),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=40)),
            ('baseoptions', self.gf('django.db.models.fields.CharField')(max_length=254, blank=True)),
            ('sortorder', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('multiplier', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('features', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('new_grid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('products', ['Product'])

        # Adding M2M table for field images on 'Product'
        db.create_table(u'products_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['products.product'], null=False)),
            ('image', models.ForeignKey(orm['products.image'], null=False))
        ))
        db.create_unique(u'products_images', ['product_id', 'image_id'])

        # Adding model 'Prodopt'
        db.create_table(u'prodopts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('qty', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('single', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('choices_orderby', self.gf('django.db.models.fields.CharField')(default='cost', max_length=20)),
            ('allowed_quantities', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=80, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Product'], db_column='productid')),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Option'], db_column='optionid')),
            ('defaultchoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Choice'], db_column='defaultchoiceid')),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('products', ['Prodopt'])

        # Adding model 'Prodoptchoice'
        db.create_table(u'prodoptchoices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pricedelta', self.gf('django.db.models.fields.FloatField')()),
            ('productoption', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Prodopt'], db_column='productoptionid')),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Choice'], db_column='choiceid')),
            ('current', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('products', ['Prodoptchoice'])


    def backwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('products_image')

        # Deleting model 'Categories'
        db.delete_table(u'categories')

        # Removing M2M table for field images on 'Categories'
        db.delete_table('categories_images')

        # Deleting model 'ChoiceCategory'
        db.delete_table(u'choicecategories')

        # Deleting model 'Choice'
        db.delete_table(u'choices')

        # Deleting model 'Option'
        db.delete_table(u'options')

        # Removing M2M table for field choices on 'Option'
        db.delete_table('options_choices')

        # Deleting model 'Product'
        db.delete_table(u'products')

        # Removing M2M table for field images on 'Product'
        db.delete_table('products_images')

        # Deleting model 'Prodopt'
        db.delete_table(u'prodopts')

        # Deleting model 'Prodoptchoice'
        db.delete_table(u'prodoptchoices')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'products.categories': {
            'Meta': {'ordering': "['sortorder', 'name']", 'object_name': 'Categories', 'db_table': "u'categories'"},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'products.choice': {
            'Meta': {'ordering': "['sortorder']", 'object_name': 'Choice', 'db_table': "u'choices'"},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'choicecategory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.ChoiceCategory']"}),
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
        'products.choicecategory': {
            'Meta': {'object_name': 'ChoiceCategory', 'db_table': "u'choicecategories'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sohigh': ('django.db.models.fields.IntegerField', [], {}),
            'solow': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'products.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'products.option': {
            'Meta': {'ordering': "['sortorder']", 'object_name': 'Option', 'db_table': "u'options'"},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'options'", 'symmetrical': 'False', 'to': "orm['products.Choice']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usage_notes': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        'products.prodopt': {
            'Meta': {'object_name': 'Prodopt', 'db_table': "u'prodopts'"},
            'allowed_quantities': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "''", 'max_length': '80', 'blank': 'True'}),
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'prodopts'", 'blank': 'True', 'through': "orm['products.Prodoptchoice']", 'to': "orm['products.Choice']"}),
            'choices_orderby': ('django.db.models.fields.CharField', [], {'default': "'cost'", 'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'defaultchoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Choice']", 'db_column': "'defaultchoiceid'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Option']", 'db_column': "'optionid'"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']", 'db_column': "'productid'"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'qty': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'single': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'products.prodoptchoice': {
            'Meta': {'object_name': 'Prodoptchoice', 'db_table': "u'prodoptchoices'"},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Choice']", 'db_column': "'choiceid'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pricedelta': ('django.db.models.fields.FloatField', [], {}),
            'productoption': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Prodopt']", 'db_column': "'productoptionid'"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'products.product': {
            'Meta': {'ordering': "['sku']", 'object_name': 'Product', 'db_table': "u'products'"},
            'baseoptions': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'baseprice': ('django.db.models.fields.FloatField', [], {}),
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Categories']", 'db_column': "'categoryid'"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'features': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'multiplier': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'new_grid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Option']", 'through': "orm['products.Prodopt']", 'symmetrical': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '40'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['products']
