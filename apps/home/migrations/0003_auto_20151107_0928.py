# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_featuredimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredimage',
            name='product',
            field=models.ForeignKey(blank=True, to='products.Product', help_text=b'Product the featured image is talking about, optional, can use caption instead', null=True),
            preserve_default=True,
        ),
    ]
