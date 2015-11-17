# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
import products.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Category Name - Capitals, spaces OK. slugified for urls.', max_length=50)),
                ('slug', models.SlugField(help_text=b'Category url name - slugified from name field.', blank=True)),
                ('title', models.CharField(help_text=b'If present, used for page title (useful for SEO).', max_length=100, blank=True)),
                ('blurb', models.TextField(help_text=b'Short description, typically a few lines, HTML OK.', blank=True)),
                ('description', models.TextField(help_text=b'Detailed description, HTML OK. Used for cetegory page.', blank=True)),
                ('comments', models.TextField(help_text=b'Internal notes and comments.  Please add dates & your initials', blank=True)),
                ('image', models.ImageField(upload_to=b'images/categories/', blank=True)),
                ('sortorder', models.IntegerField(default=100)),
                ('published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['sortorder', 'name'],
                'db_table': 'categories',
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('supplier', models.IntegerField(blank=True)),
                ('price', models.FloatField(blank=True)),
                ('cost', models.FloatField()),
                ('sortorder', models.IntegerField()),
                ('multiplier', models.IntegerField(blank=True)),
                ('comment', models.CharField(max_length=80, blank=True)),
                ('blurb', models.TextField(help_text=b'Short description, typically a few lines, HTML OK.', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('published', models.NullBooleanField(default=True)),
            ],
            options={
                'ordering': ['sortorder'],
                'db_table': 'choices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChoiceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('sohigh', models.IntegerField(verbose_name=b'High Sort Order')),
                ('solow', models.IntegerField(verbose_name=b'Low Sort Order')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'choicecategories',
                'verbose_name_plural': 'Choice Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200)),
                ('title', models.CharField(help_text=b'If present, used for mouseover title / alt.', max_length=70, blank=True)),
                ('caption', models.CharField(help_text=b'If present, used for image caption.', max_length=200, blank=True)),
                ('published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Option Name - shown in config grid unless overriden by ProdutOption name.', max_length=50)),
                ('usage_notes', models.CharField(help_text=b'Usage notes - used internally to disambiguate options with the same name.', max_length=80, blank=True)),
                ('sortorder', models.IntegerField(help_text=b'Sort order for this option - The options appear ordered by this in the config grid.')),
                ('blurb', models.TextField(help_text=b'Short description, typically a few lines, HTML OK.', blank=True)),
                ('description', models.TextField(help_text=b'Detailed description, HTML OK.', blank=True)),
                ('comments', models.TextField(help_text=b'Internal notes and comments.  Please add dates & your initials', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('choices', models.ManyToManyField(help_text=b'"OptionList" of Choices - NEW July 2011 for POOL architecture.', related_name='options', to='products.Choice')),
            ],
            options={
                'ordering': ['sortorder'],
                'db_table': 'options',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prodopt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name to display in config grid - blank uses the Option name by default.', max_length=64, blank=True)),
                ('qty', models.IntegerField(default=1, help_text=b'The <b>Option Quantity</b> - the number of lines of this option to display in config grid. Defaults to 1.')),
                ('single', models.BooleanField(default=False, help_text=b'If checked, there are no OptionChoices, the defaultchoice is the only possible choice.')),
                ('required', models.BooleanField(default=False, help_text=b'If checked, this option will not have a "none" choice.  If false, a "none" choice will be available.')),
                ('choices_orderby', models.CharField(default=b'cost', help_text=b'Name to display in config grid - blank uses the Option name by default.', max_length=20, choices=[(b'cost', b'cost'), (b'sortorder', b'sortorder')])),
                ('allowed_quantities', models.CommaSeparatedIntegerField(default=b'', help_text=b"The allowed <b>Choice Quantities</b> - a comma-separated list of integers, eg '1,2,4' etc. Blank means don't display a quantity box.", max_length=80, blank=True)),
                ('published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'prodopts',
                'verbose_name': 'Product Option',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prodoptchoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pricedelta', models.FloatField()),
                ('current', models.CharField(max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('choice', models.ForeignKey(to='products.Choice', db_column=b'choiceid')),
                ('productoption', models.ForeignKey(to='products.Prodopt', db_column=b'productoptionid')),
            ],
            options={
                'db_table': 'prodoptchoices',
                'verbose_name': 'Product-Option Choice',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Product name - by convention is "eRacks/<sku>".', max_length=50)),
                ('sku', models.CharField(help_text=b"Our sku, also used as our Model Number or MPN (Manufacturer's Part Number).", unique=True, max_length=50)),
                ('baseprice', models.FloatField(help_text=b'Base / baseline price for this model.')),
                ('cost', models.FloatField(help_text=b'Our cost - note that this field is not updated as our costs change, so is likely to be old.')),
                ('weight', models.IntegerField(default=40, help_text=b'Total shipping weight in lbs - defaults to 40.')),
                ('baseoptions', models.CharField(max_length=254, blank=True)),
                ('sortorder', models.IntegerField(default=0)),
                ('multiplier', models.IntegerField(help_text=b'Markup multiplier to set the sale price for the product.', blank=True)),
                ('blurb', models.TextField(help_text=b'Short description, typically a few lines, HTML OK.', blank=True)),
                ('description', models.TextField(help_text=b'Detailed description, HTML OK.', blank=True)),
                ('features', models.TextField(help_text=b'Features, shown on Product Features tab.', blank=True)),
                ('comments', models.TextField(help_text=b'Internal notes and comments.  Please add dates & your initials', blank=True)),
                ('link', models.CharField(max_length=150, blank=True)),
                ('image', models.CharField(max_length=300, blank=True)),
                ('title', models.CharField(help_text=b'If present, used for product page title (useful for SEO). Only for newer Django (non-Zope) products.', max_length=100, blank=True)),
                ('new_grid', models.BooleanField(default=False, help_text=b'If true, use the newer django-based grid to present the product grid view to the customer.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=True, help_text=b'Filters whether product is shown in queries.')),
                ('category', models.ForeignKey(db_column=b'categoryid', to='products.Categories', help_text=b'Legacy Zope Category for this product.')),
                ('images', models.ManyToManyField(to='products.Image', blank=True)),
                ('options', models.ManyToManyField(help_text=b'ProductOptions for this product - used by BOTH legacy Zope PO-POC architecture, and the new Django PO-OL architecture.', to='products.Option', through='products.Prodopt')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ['sku'],
                'db_table': 'products',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='prodopt',
            name='choices',
            field=models.ManyToManyField(help_text=b'Legacy ProductOptionChoices - overrides OptionChoice list if present - Feb2012 JJW', related_name='prodopts', through='products.Prodoptchoice', to='products.Choice', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prodopt',
            name='defaultchoice',
            field=models.ForeignKey(db_column=b'defaultchoiceid', default=products.models.get_none_choice, to='products.Choice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prodopt',
            name='option',
            field=models.ForeignKey(to='products.Option', db_column=b'optionid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prodopt',
            name='product',
            field=models.ForeignKey(to='products.Product', db_column=b'productid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='choice',
            name='choicecategory',
            field=models.ForeignKey(verbose_name=b'category', to='products.ChoiceCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categories',
            name='images',
            field=models.ManyToManyField(to='products.Image', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categories',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
