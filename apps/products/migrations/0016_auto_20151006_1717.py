# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20151006_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='price',
            field=models.FloatField(help_text=b'Override cost-based calculated price with this (not used much)', null=True, blank=True),
            preserve_default=True,
        ),
    ]
