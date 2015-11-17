# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20151003_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='supplier',
        ),
        migrations.AddField(
            model_name='choice',
            name='source',
            field=models.CharField(max_length=80, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choice',
            name='cost',
            field=models.FloatField(help_text=b'Our internal cost, used to calculate prices & differences'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choice',
            name='multiplier',
            field=models.IntegerField(help_text=b'Override internal multiplier with this (not used much, can be 0 or 1 too)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choice',
            name='price',
            field=models.FloatField(help_text=b'Override cost-based calculated price with this (not used much)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choice',
            name='published',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
