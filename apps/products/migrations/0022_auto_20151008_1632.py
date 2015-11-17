# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_categoryimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryimage',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=200),
            preserve_default=True,
        ),
    ]
