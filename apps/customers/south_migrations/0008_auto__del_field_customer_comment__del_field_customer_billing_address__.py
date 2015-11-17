# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Deleting field 'Customer.comment'
        db.rename_column(u'customers', 'comment', 'comments')

        # Deleting field 'Customer.billing_address'
        db.delete_column(u'customers', 'billing_address')

        # Deleting field 'Customer.name'
        db.rename_column(u'customers', 'name', 'organization_name')

        # Deleting field 'Customer.primarycreditcard'
        db.delete_column(u'customers', 'primarycreditcard')

        # Deleting field 'Customer.primaryshipping'
        db.delete_column(u'customers', 'primaryshipping')

        # Deleting field 'Customer.maillist'
        db.delete_column(u'customers', 'maillist')

        # Deleting field 'Customer.dept'
        db.rename_column(u'customers', 'dept', 'department')

        # Deleting field 'Customer.primarybilling'
        db.delete_column(u'customers', 'primarybilling')

        # Deleting field 'Customer.modified'
        db.rename_column(u'customers', 'modified', 'updated')

        # Deleting field 'Customer.shipping_address'
        db.delete_column(u'customers', 'shipping_address')

        # Adding field 'Customer.organization_name'
        #db.add_column(u'customers', 'organization_name', self.gf('django.db.models.fields.CharField')(default='', max_length=80), keep_default=False)

        # Adding field 'Customer.department'
        #db.add_column(u'customers', 'department', self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True), keep_default=False)

        # Adding field 'Customer.comments'
        #db.add_column(u'customers', 'comments', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Customer.updated'
        #db.add_column(u'customers', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=0, blank=True), keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Customer.comment'
        raise RuntimeError("Cannot reverse this migration. 'Customer.comment' and its values cannot be restored.")

        # Adding field 'Customer.billing_address'
        db.add_column(u'customers', 'billing_address', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'Customer.name'
        raise RuntimeError("Cannot reverse this migration. 'Customer.name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Customer.primarycreditcard'
        raise RuntimeError("Cannot reverse this migration. 'Customer.primarycreditcard' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Customer.primaryshipping'
        raise RuntimeError("Cannot reverse this migration. 'Customer.primaryshipping' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Customer.maillist'
        raise RuntimeError("Cannot reverse this migration. 'Customer.maillist' and its values cannot be restored.")

        # Adding field 'Customer.dept'
        db.add_column(u'customers', 'dept', self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'Customer.primarybilling'
        raise RuntimeError("Cannot reverse this migration. 'Customer.primarybilling' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Customer.modified'
        raise RuntimeError("Cannot reverse this migration. 'Customer.modified' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Customer.shipping_address'
        raise RuntimeError("Cannot reverse this migration. 'Customer.shipping_address' and its values cannot be restored.")

        # Deleting field 'Customer.organization_name'
        db.delete_column(u'customers', 'organization_name')

        # Deleting field 'Customer.department'
        db.delete_column(u'customers', 'department')

        # Deleting field 'Customer.comments'
        db.delete_column(u'customers', 'comments')

        # Deleting field 'Customer.updated'
        db.delete_column(u'customers', 'updated')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 5, 16, 25, 2, 12973)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 5, 16, 25, 2, 12760)'}),
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
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'customers.customerimage': {
            'Meta': {'ordering': "['sortorder']", 'object_name': 'CustomerImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'customers.testimonial': {
            'Meta': {'ordering': "['sortorder']", 'object_name': 'Testimonial'},
            'attribution': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'quote': ('django.db.models.fields.TextField', [], {}),
            'sortorder': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['customers']
