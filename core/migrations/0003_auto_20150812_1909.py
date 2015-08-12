# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150725_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailmatchabilityupgrade',
            name='cability_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailmatchowneritem',
            name='citem_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailmatchplayer',
            name='chero_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
