# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'County, plus city in parens for rate exceptions', unique=True, max_length=150)),
                ('county', models.CharField(help_text=b'County name only', max_length=50)),
                ('tax', models.DecimalField(help_text=b'Total CA Sales Tax rate', max_digits=5, decimal_places=2)),
                ('cities', models.CommaSeparatedIntegerField(help_text=b'Comma-separated list of cities within the county for which this tax rate applies', max_length=3000, blank=True)),
                ('count', models.IntegerField(help_text=b'Count of cities, used to determine the need for the city to be added to the county for uniqueness')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'catax',
                'verbose_name': 'CA Tax',
                'verbose_name_plural': 'CA Taxes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='catax',
            unique_together=set([('county', 'tax')]),
        ),
    ]
