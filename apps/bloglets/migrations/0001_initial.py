# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'Date updated')),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name=b'Date published')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'Date updated')),
                ('published', models.BooleanField(default=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='bloglets.Category')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
            bases=(models.Model,),
        ),
    ]
