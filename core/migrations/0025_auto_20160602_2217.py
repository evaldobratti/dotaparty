# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20160602_2213'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ability',
        ),
        migrations.AlterField(
            model_name='account',
            name='account_id',
            field=models.BigIntegerField(unique=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='detailmatch',
            name='match_id',
            field=models.BigIntegerField(unique=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='detailmatchplayer',
            name='account_id',
            field=models.BigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='hero',
            name='hero_id',
            field=models.SmallIntegerField(unique=True, db_index=True),
        ),
    ]
