# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20151008_1725'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]
