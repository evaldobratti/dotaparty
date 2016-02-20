# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20160122_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='localized_name',
            field=models.CharField(max_length=400),
        ),
    ]
