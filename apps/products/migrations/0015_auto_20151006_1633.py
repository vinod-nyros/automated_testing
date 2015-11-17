# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20151006_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='comment',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
