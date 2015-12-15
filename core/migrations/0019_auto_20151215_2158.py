# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20151214_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailmatch',
            name='skill',
            field=models.PositiveIntegerField(null=True, choices=[(None, b'To be determined'), (1, b'Normal'), (2, b'High'), (3, b'Very High'), (4, b'Not determined')]),
        ),
    ]
