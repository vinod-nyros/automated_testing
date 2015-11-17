# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20150203_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.SlugField(help_text=b'Category url name - slugified from name field.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choice',
            name='comment',
            field=models.TextField(max_length=80, blank=True),
            preserve_default=True,
        ),
    ]
