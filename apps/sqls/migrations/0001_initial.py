# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sql',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=160)),
                ('updates', models.BooleanField(verbose_name=b'Updates DB')),
                ('sql', models.TextField()),
                ('parm1', models.CharField(max_length=30, blank=True)),
                ('parm2', models.CharField(max_length=30, blank=True)),
                ('parm3', models.CharField(max_length=30, blank=True)),
                ('parm4', models.CharField(max_length=30, blank=True)),
                ('parm5', models.CharField(max_length=30, blank=True)),
                ('notes', models.TextField(max_length=30, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
