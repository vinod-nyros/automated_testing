# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20141104_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importedorder',
            name='reftyp',
            field=models.CharField(help_text=b'Referral type for this order', max_length=10, choices=[(b'', b'Please Select'), (b'google', b'Google search'), (b'googlead', b'Google Ad'), (b'yahoo', b'Yahoo'), (b'Facebook', b'Facebook'), (b'Twitter', b'Twitter'), (b'YouTube', b'YouTube'), (b'Online Web magazine', b'Online Web magazine(please enter it below)'), (b'Phoronix', b'Phoronix'), (b'search', b'Other search engine (please enter below)'), (b'Github', b'Github(Please enter who below)'), (b'The Var Guy top 50', b'The Var Guy top 50'), (b'press', b'Press release'), (b'repeat', b'Repeat business'), (b'referral', b'Referral or word-of-mouth (please enter below)'), (b'flyer', b'Brochure or flyer (please enter promo code below)'), (b'conf', b'Conference or Trade Show (please enter below)'), (b'list', b'Mailing list or newsgroup (please enter below)'), (b'project', b'Open-Source site (OpenBSD, Zope, etc - enter below)'), (b'mag', b'Magazine article (please enter mag and month/yr below)'), (b'magad', b'Magazine ad (please enter mag and month/yr below)'), (b'blog', b'Link from portal or blog (please enter below)'), (b'website', b'Other link or website (please enter below)'), (b'auction', b'Auction site (eBay, UBid, etc - please enter below)'), (b'other', b'Other - please enter below')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='referral_type',
            field=models.CharField(default=b'Please Select', help_text=b'How did you hear of us?', max_length=80, choices=[(b'', b'Please Select'), (b'google', b'Google search'), (b'googlead', b'Google Ad'), (b'yahoo', b'Yahoo'), (b'Facebook', b'Facebook'), (b'Twitter', b'Twitter'), (b'YouTube', b'YouTube'), (b'Online Web magazine', b'Online Web magazine(please enter it below)'), (b'Phoronix', b'Phoronix'), (b'search', b'Other search engine (please enter below)'), (b'Github', b'Github(Please enter who below)'), (b'The Var Guy top 50', b'The Var Guy top 50'), (b'press', b'Press release'), (b'repeat', b'Repeat business'), (b'referral', b'Referral or word-of-mouth (please enter below)'), (b'flyer', b'Brochure or flyer (please enter promo code below)'), (b'conf', b'Conference or Trade Show (please enter below)'), (b'list', b'Mailing list or newsgroup (please enter below)'), (b'project', b'Open-Source site (OpenBSD, Zope, etc - enter below)'), (b'mag', b'Magazine article (please enter mag and month/yr below)'), (b'magad', b'Magazine ad (please enter mag and month/yr below)'), (b'blog', b'Link from portal or blog (please enter below)'), (b'website', b'Other link or website (please enter below)'), (b'auction', b'Auction site (eBay, UBid, etc - please enter below)'), (b'other', b'Other - please enter below')]),
            preserve_default=True,
        ),
    ]
