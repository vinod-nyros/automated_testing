# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20151006_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='multiplier',
        ),
        migrations.AlterField(
            model_name='choice',
            name='multiplier',
            field=models.IntegerField(help_text=b'Override internal multiplier with this if >0 (not used much, can be 1 to sell at cost)', null=True),
            preserve_default=True,
        ),
    ]
