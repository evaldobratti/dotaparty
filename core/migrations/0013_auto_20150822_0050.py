# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from core import parameters

def create_parameters(apps, schema_editor):
    Parameter = apps.get_model("core", "Parameter")

    Parameter.objects.create(name=parameters.LAST_MATCH_ID_SKILL_VERY_HIGH, value=None)
    Parameter.objects.create(name=parameters.LAST_MATCH_ID_SKILL_HIGH, value=None)
    Parameter.objects.create(name=parameters.LAST_MATCH_ID_SKILL_NORMAL, value=None)
    Parameter.objects.create(name=parameters.INTERESTED_ACCOUNTS_IDS, value='[88738111]')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150822_0050'),
    ]

    operations = [
        migrations.RunPython(create_parameters),
    ]
