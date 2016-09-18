# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_proxy_timeouts'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='history',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]
