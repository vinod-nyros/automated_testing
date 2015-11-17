# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20150111_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['sortorder', 'sku']},
        ),
        migrations.AddField(
            model_name='choicecategory',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='products.ChoiceCategory', null=True),
            preserve_default=True,
        ),
    ]
