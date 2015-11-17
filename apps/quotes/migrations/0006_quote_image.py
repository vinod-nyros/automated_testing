# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_auto_20150111_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
