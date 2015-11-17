# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20151006_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodoptchoice',
            name='current',
            field=models.CharField(max_length=1, null=True),
            preserve_default=True,
        ),
    ]
