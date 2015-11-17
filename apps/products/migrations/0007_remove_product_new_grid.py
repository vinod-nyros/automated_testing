# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20150217_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='new_grid',
        ),
    ]
