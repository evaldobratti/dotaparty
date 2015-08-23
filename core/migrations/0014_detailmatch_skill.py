# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150822_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailmatch',
            name='skill',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
