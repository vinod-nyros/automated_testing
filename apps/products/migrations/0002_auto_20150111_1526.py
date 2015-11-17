# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='options',
            field=models.ManyToManyField(related_name='+', to='products.Option'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choice',
            name='choicecategory',
            field=models.ForeignKey(default=products.models.get_misc_choice_category, verbose_name=b'category', to='products.ChoiceCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='option',
            name='choices',
            field=models.ManyToManyField(help_text=b'"OptionList" of Choices - NEW July 2011 for POOL architecture.', related_name='+', to='products.Choice'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='prodopt',
            name='defaultchoice',
            field=models.ForeignKey(db_column=b'defaultchoiceid', default=products.models.get_none_choice, to='products.Choice', help_text=b"Default choice from list of option-choices or legacy POCs - <b><span style='color:red'>SAVE TWICE to set this correctly</span></b>, otherwise fault will occur on ajax product update!"),
            preserve_default=True,
        ),
    ]
