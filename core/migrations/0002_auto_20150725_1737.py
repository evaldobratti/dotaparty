# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='current_update',
            field=models.ForeignKey(related_name='current_update', to='core.AccountUpdate', null=True),
        ),
    ]
