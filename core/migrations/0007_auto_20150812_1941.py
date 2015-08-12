# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150812_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detailmatchabilityupgrade',
            name='ability',
        ),
        migrations.RemoveField(
            model_name='detailmatchowneritem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='detailmatchplayer',
            name='hero',
        ),
    ]
