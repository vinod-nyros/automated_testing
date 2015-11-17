# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqls', '0002_auto_20141104_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sql',
            name='notes',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
