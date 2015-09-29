# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20150827_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='matches_download_required',
            field=models.BooleanField(default=False),
        ),
    ]
