# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_auto_20151008_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', filebrowser.fields.FileBrowseField(unique=True, max_length=200)),
                ('title', models.CharField(help_text=b'If present, used for mouseover title / alt.', max_length=70, blank=True)),
                ('caption', models.CharField(help_text=b'If present, used for image caption.', max_length=200, blank=True)),
                ('category', models.ForeignKey(to='products.Categories')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
