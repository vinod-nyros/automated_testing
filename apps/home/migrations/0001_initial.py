# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200)),
                ('link', models.CharField(help_text=b'Product or page to link to - relative links OK', max_length=100)),
                ('title', models.CharField(help_text=b'Mouseover title - optional', max_length=100, blank=True)),
                ('caption', models.CharField(help_text=b'Image / Slide caption - optional, shown across bottom of image, such as &lt;h2>My Caption&lt;/h2>', max_length=100, blank=True)),
                ('sortorder', models.IntegerField(default=100, help_text=b'Default order the slideshow is shown in')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['sortorder'],
            },
            bases=(models.Model,),
        ),
    ]
