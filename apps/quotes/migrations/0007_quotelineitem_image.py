# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0006_quote_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotelineitem',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
