# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20150923_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
