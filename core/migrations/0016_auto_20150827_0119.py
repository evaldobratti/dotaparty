# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150822_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailmatchplayer',
            name='leaver_status',
            field=models.ForeignKey(to='core.LeaverStatus', null=True),
        ),
    ]
