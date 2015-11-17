# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sql',
            name='updates',
            field=models.BooleanField(default=False, help_text=b'Updates DB'),
            preserve_default=True,
        ),
    ]
