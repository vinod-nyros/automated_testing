# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20150927_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicecategory',
            name='sohigh',
            field=models.IntegerField(default=0, verbose_name=b'High Sort Order'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choicecategory',
            name='solow',
            field=models.IntegerField(default=0, verbose_name=b'Low Sort Order'),
            preserve_default=True,
        ),
    ]
