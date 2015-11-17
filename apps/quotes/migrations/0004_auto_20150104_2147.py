# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from quotes.models import Quote
from quotes.models import QuoteLineItem

def remove_null_quote(apps, schema_editor):
    Quote = apps.get_model("quotes", "Quote")
    for i in Quote.objects.filter(comments=None):
        i.comments=''
        i.save()
        print "saved"
def remove_null_quoteline(apps, schema_editor):
    QuoteLineItem = apps.get_model("quotes", "QuoteLineItem")
    for j in QuoteLineItem.objects.filter(comments=None):
        j.comments=''
        j.save()
        print "saved"
    
class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_auto_20150101_2041'),
    ]

    operations = [
        migrations.RunPython(remove_null_quote),
        migrations.RunPython(remove_null_quoteline),
        migrations.RemoveField(
            model_name='quotelineitem',
            name='customer_reference',
        ),
        migrations.AlterField(
            model_name='quote',
            name='comments',
            field=models.TextField(default=b'', help_text=b'comments for quotes ', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quotelineitem',
            name='comments',
            field=models.TextField(default=b'', help_text=b'comments for quote line item ', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quotelineitem',
            name='shipping',
            field=models.FloatField(help_text=b'Estimated weight - lbs', blank=True),
            preserve_default=True,
        ),
    ]
