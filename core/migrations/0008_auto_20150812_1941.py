# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150812_1941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailmatchabilityupgrade',
            old_name='cability_id',
            new_name='ability_id',
        ),
        migrations.RenameField(
            model_name='detailmatchowneritem',
            old_name='citem_id',
            new_name='item_id',
        ),
        migrations.RenameField(
            model_name='detailmatchplayer',
            old_name='chero_id',
            new_name='hero_id',
        ),
    ]
