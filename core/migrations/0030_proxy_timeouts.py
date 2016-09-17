# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20160917_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='timeouts',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
