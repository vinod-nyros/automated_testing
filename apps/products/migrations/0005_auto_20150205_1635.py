# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20150205_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='comment',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choice',
            name='name',
            field=models.CharField(max_length=80),
            preserve_default=True,
        ),
    ]
