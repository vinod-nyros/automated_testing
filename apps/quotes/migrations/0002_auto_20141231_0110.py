# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='comments',
            field=models.TextField(help_text=b'comments for quotes ', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quotelineitem',
            name='comments',
            field=models.TextField(help_text=b'comments for quote line item ', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quotelineitem',
            name='customer_reference',
            field=models.CharField(help_text=b'Other customer reference number, RFQ, contact name, etc', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quotelineitem',
            name='shipping',
            field=models.FloatField(default=0.0, help_text=b'Estimated weight - lbs', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quote',
            name='customer_reference',
            field=models.CharField(help_text=b'Other customer reference number, RFQ, contact name, etc', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
