# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20151102_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountupdate',
            name='persona_state_flags',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='accountupdate',
            name='primary_clan_id',
            field=models.BigIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='accountupdate',
            name='sequential',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='accountupdate',
            unique_together=set([('account', 'persona_name', 'url_avatar', 'url_avatar_medium', 'url_avatar_full', 'primary_clan_id', 'persona_state_flags')]),
        ),
    ]
