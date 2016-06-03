# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20160220_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detailmatchabilityupgrade',
            name='player',
        ),
        migrations.DeleteModel(
            name='DetailMatchAbilityUpgrade',
        ),
    ]
