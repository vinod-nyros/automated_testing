# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quote_number', models.CharField(help_text=b'eRacks quote id - letters/numbers/underscore/dashes ok, no spaces', unique=True, max_length=20)),
                ('valid_for', models.IntegerField(default=10, help_text=b'Number of days the quote is valid for')),
                ('purchase_order', models.CharField(help_text=b'Customer Purchase Order number, etc', max_length=20, blank=True)),
                ('customer_reference', models.CharField(help_text=b'Other customer reference number, RFQ, contact name, etc', max_length=30, blank=True)),
                ('terms', models.CharField(default=b'ccard', help_text=b'Net 5, Wire Transfer, ccard, etc', max_length=20)),
                ('discount', models.FloatField(default=0, help_text=b'Dollars or percent, according to type', blank=True)),
                ('discount_type', models.CharField(default=b'$', max_length=1, blank=True, choices=[(b'$', b'Dollars'), (b'%', b'Percent')])),
                ('shipping', models.FloatField(help_text=b'Estimated weight - lbs', blank=True)),
                ('shipping_method', models.CharField(help_text=b'UPS, FedEx, Freight, 3-Day, etc', max_length=40, blank=True)),
                ('target', models.FloatField(help_text=b"The customer's budget, or where the customer would like the quote to be")),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(default=2, to=settings.AUTH_USER_MODEL, help_text=b'Manager or admin person approving quote')),
                ('customer', models.ForeignKey(blank=True, to='customers.Customer', help_text=b'click "+" to create new', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuoteLineItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.CharField(help_text=b'eRacks Model name, eg "OPTERNATOR", or make one up for custom quotes', max_length=60)),
                ('quantity', models.IntegerField()),
                ('description', models.TextField(help_text=b'Start with a line for general description, then one config item per line for components')),
                ('cost', models.FloatField(help_text=b'our cost')),
                ('price', models.FloatField(help_text=b'customer price')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('quote', models.ForeignKey(to='quotes.Quote')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
