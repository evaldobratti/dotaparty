# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from core import parameters

def create_parameters(apps, schema_editor):
    Parameter = apps.get_model("core", "Parameter")

    if len(Parameter.objects.filter(name=parameters.INTERESTED_ACCOUNTS_IDS)) == 0:
        Parameter.objects.create(name=parameters.INTERESTED_ACCOUNTS_IDS, value='[]')

    if len(Parameter.objects.filter(name=parameters.LAST_MATCH_SEQ_NUM)) == 0:
        Parameter.objects.create(name=parameters.LAST_MATCH_SEQ_NUM, value=None)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150822_0050'),
    ]

    operations = [
        migrations.RunPython(create_parameters),
    ]
