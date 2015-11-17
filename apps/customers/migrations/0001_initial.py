# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
import django_countries.fields
import userena.models
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(help_text=b'Address nickname/description - home, office, manufacturing, etc', max_length=80, blank=True)),
                ('name', models.CharField(help_text=b'Name (if different than above)', max_length=80, blank=True)),
                ('address1', models.CharField(help_text=b'Street name & number', max_length=80)),
                ('address2', models.CharField(help_text=b'Apt, suite, additional info', max_length=80, blank=True)),
                ('city', models.CharField(help_text=b'City, town, village, etc', max_length=80)),
                ('state', models.CharField(help_text=b'State, Province, or region', max_length=50, choices=[(b'', b'Please Select'), (b'AL', b'AL (Alabama)'), (b'AK', b'AK (Alaska)'), (b'AS', b'AS (American Samoa)'), (b'AZ', b'AZ (Arizona)'), (b'AR', b'AR (Arkansas)'), (b'AE', b'AE (Armed Forces Europe)'), (b'AA', b'AA (Armed Forces Americas)'), (b'AP', b'AP (Armed Forces Pacific)'), (b'CA', b'CA (California)'), (b'CO', b'CO (Colorado)'), (b'CT', b'CT (Connecticut)'), (b'DE', b'DE (Delaware)'), (b'DC', b'DC (District of Columbia)'), (b'FM', b'FM (Federated States of Micronesia)'), (b'FL', b'FL (Florida)'), (b'GA', b'GA (Georgia)'), (b'GU', b'GU (Guam)'), (b'HI', b'HI (Hawaii)'), (b'ID', b'ID (Idaho)'), (b'IL', b'IL (Illinois)'), (b'IN', b'IN (Indiana)'), (b'IA', b'IA (Iowa)'), (b'KS', b'KS (Kansas)'), (b'KY', b'KY (Kentucky)'), (b'LA', b'LA (Louisiana)'), (b'ME', b'ME (Maine)'), (b'MH', b'MH (Marshall Islands)'), (b'MD', b'MD (Maryland)'), (b'MA', b'MA (Massachusetts)'), (b'MI', b'MI (Michigan)'), (b'MN', b'MN (Minnesota)'), (b'MS', b'MS (Mississippi)'), (b'MO', b'MO (Missouri)'), (b'MT', b'MT (Montana)'), (b'NE', b'NE (Nebraska)'), (b'NV', b'NV (Nevada)'), (b'NH', b'NH (New Hampshire)'), (b'NJ', b'NJ (New Jersey)'), (b'NM', b'NM (New Mexico)'), (b'NY', b'NY (New York)'), (b'NC', b'NC (North Carolina)'), (b'ND', b'ND (North Dakota)'), (b'MP', b'MP (Northern Mariana Islands)'), (b'OH', b'OH (Ohio)'), (b'OK', b'OK (Oklahoma)'), (b'OR', b'OR (Oregon)'), (b'PW', b'PW (Palau)'), (b'PA', b'PA (Pennsylvania)'), (b'PR', b'PR (Puerto Rico)'), (b'RI', b'RI (Rhode Island)'), (b'SC', b'SC (South Carolina)'), (b'SD', b'SD (South Dakota)'), (b'TN', b'TN (Tennessee)'), (b'TX', b'TX (Texas)'), (b'UT', b'UT (Utah)'), (b'VT', b'VT (Vermont)'), (b'VI', b'VI (Virgin Islands)'), (b'VA', b'VA (Virginia)'), (b'WA', b'WA (Washington)'), (b'WV', b'WV (West Virginia)'), (b'WI', b'WI (Wisconsin)'), (b'WY', b'WY (Wyoming)')])),
                ('zip', models.CharField(help_text=b'Zip or postal code', max_length=20)),
                ('country', django_countries.fields.CountryField(default=b'US', help_text=b'Choose your country', max_length=2)),
                ('phone', models.CharField(help_text=b'Phone number for this address, if different from primary', max_length=20, blank=True)),
                ('email', models.CharField(help_text=b'email address for this address, if different from primary', max_length=100, blank=True)),
                ('type', models.CharField(help_text=b'Address type - choose, or use nickname if "other"', max_length=50, choices=[(b'shipping', b'Shipping'), (b'billing', b'Billing'), (b'both', b'Both shipping and billing'), (b'other', b'Alternate address')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=True, help_text=b"Use this to unpublish, don't delete")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'closed', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('organization', models.CharField(help_text=b'Company, School, University, Non-profit organization, club, etc', max_length=80, blank=True)),
                ('title', models.CharField(help_text=b'Title at the organization', max_length=80, blank=True)),
                ('department', models.CharField(help_text=b'Department within the organization', max_length=80, blank=True)),
                ('email', models.CharField(help_text=b'Primary eMail address', max_length=160)),
                ('email2', models.CharField(help_text=b'Alternate eMail address', max_length=160, blank=True)),
                ('phone', models.CharField(help_text=b'Primary phone number with area code (and country code if not US)', max_length=40)),
                ('phone2', models.CharField(help_text=b'Alternate phone number', max_length=40, blank=True)),
                ('comments', models.TextField(help_text=b'Internal notes, customer comments, record of phone conversations', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=True, help_text=b'Use this for mailing list opt-out')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'customers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200)),
                ('link', models.URLField()),
                ('title', models.CharField(max_length=100, blank=True)),
                ('caption', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('sortorder', models.IntegerField(default=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(blank=True, to='customers.Customer', null=True)),
            ],
            options={
                'ordering': ['sortorder'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quote', models.TextField(help_text=b"Don't include quotes or italics. Some limited html OK.")),
                ('attribution', models.TextField(help_text=b'Generally just initials, city, and compeny (Link and some html OK)')),
                ('sortorder', models.IntegerField(default=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['sortorder'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(to='customers.Customer'),
            preserve_default=True,
        ),
    ]
