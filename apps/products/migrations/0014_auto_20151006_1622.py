# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20151006_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='multiplier',
            field=models.IntegerField(help_text=b'Override internal multiplier with this (not used much, can be 0 or 1 too)', null=True),
            preserve_default=True,
        ),
    ]
