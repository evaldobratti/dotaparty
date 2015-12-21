# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20151215_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ability',
            name='ability_id',
            field=models.SmallIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='cluster_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='gamemode',
            name='game_mode_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='hero',
            name='hero_id',
            field=models.SmallIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='lobbytype',
            name='lobby_type_id',
            field=models.IntegerField(unique=True),
        ),
    ]
