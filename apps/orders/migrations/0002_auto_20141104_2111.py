# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='agree_to_terms',
            field=models.BooleanField(default=False, help_text=b'Customer agreed to terms and accepted EULA'),
            preserve_default=True,
        ),
    ]
