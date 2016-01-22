# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20151226_2258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='datetime_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='detailmatch',
            old_name='datetime_created',
            new_name='created_at',
        ),
    ]
