# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20151221_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='datetime_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 26, 22, 58, 30, 272053), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailmatch',
            name='datetime_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 26, 22, 58, 46, 313263), auto_now_add=True),
            preserve_default=False,
        ),
    ]
