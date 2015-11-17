# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20151030_1552'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredimage',
            name='product',
            field=models.ForeignKey(to='products.Product', help_text=b'Product the featured image is talking about, optional, can use caption instead', null=True),
            preserve_default=True,
        ),
    ]
