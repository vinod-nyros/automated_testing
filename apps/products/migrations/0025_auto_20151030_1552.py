# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_delete_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryimage',
            name='sortorder',
            field=models.IntegerField(default=100, help_text=b'Top one is the default image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(related_name='images', to='products.Product'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productimage',
            name='sortorder',
            field=models.IntegerField(default=100, help_text=b'Top one is the default image'),
            preserve_default=True,
        ),
    ]
