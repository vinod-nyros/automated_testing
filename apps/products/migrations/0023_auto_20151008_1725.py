# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20151008_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text=b'If present, used for mouseover title / alt.', max_length=70, blank=True)),
                ('caption', models.CharField(help_text=b'If present, used for image caption.', max_length=200, blank=True)),
                ('sortorder', models.IntegerField(default=100)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='categories',
            name='image',
        ),
        migrations.RemoveField(
            model_name='categories',
            name='images',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.AddField(
            model_name='categoryimage',
            name='sortorder',
            field=models.IntegerField(default=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='categoryimage',
            name='category',
            field=models.ForeignKey(related_name='images', to='products.Categories'),
            preserve_default=True,
        ),
    ]
