# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20151006_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodoptchoice',
            name='pricedelta',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
