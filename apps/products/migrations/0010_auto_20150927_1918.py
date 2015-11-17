# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20150927_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicecategory',
            name='abbrev',
            field=models.CharField(help_text=b'For prefixes on choice display names - typically 3 chars, uppercase', max_length=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choicecategory',
            name='name',
            field=models.CharField(max_length=80),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=filebrowser.fields.FileBrowseField(unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
