# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_auto_20150104_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotelineitem',
            name='shipping',
            field=models.FloatField(default=45, help_text=b'Estimated weight - lbs', blank=True),
            preserve_default=True,
        ),
    ]
