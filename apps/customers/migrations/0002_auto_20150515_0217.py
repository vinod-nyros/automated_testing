# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(help_text=b'Name (if different than above)', max_length=80),
            preserve_default=True,
        ),
    ]
