# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150822_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='value',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
