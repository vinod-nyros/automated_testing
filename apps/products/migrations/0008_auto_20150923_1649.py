# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_product_new_grid'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='meta_description',
            field=models.TextField(help_text=b'Meta description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categories',
            name='meta_keywords',
            field=models.TextField(help_text=b'Meta keywords', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categories',
            name='meta_title',
            field=models.CharField(help_text=b'Meta title', max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description',
            field=models.TextField(help_text=b'Meta description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='meta_keywords',
            field=models.TextField(help_text=b'Meta keywords', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='meta_title',
            field=models.CharField(help_text=b'Meta title', max_length=512, blank=True),
            preserve_default=True,
        ),
    ]
